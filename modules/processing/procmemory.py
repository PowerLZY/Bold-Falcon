# Copyright (C) 2010-2013 Claudio Guarnieri.
# Copyright (C) 2014-2016 Cuckoo Foundation.
# Copyright (C) 2020-2021 PowerLZY.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import hashlib
import logging
import os
import re
import struct

from lib.cuckoo.common.abstracts import Processing
from lib.cuckoo.common.objects import File

try:
    import pefile
    HAVE_PEFILE = True
except ImportError:
    HAVE_PEFILE = False

log = logging.getLogger(__name__)

PAGE_READONLY = 0x00000002
PAGE_READWRITE = 0x00000004
PAGE_WRITECOPY = 0x00000008
PAGE_EXECUTE = 0x00000010
PAGE_EXECUTE_READ = 0x00000020
PAGE_EXECUTE_READWRITE = 0x00000040
PAGE_EXECUTE_WRITECOPY = 0x00000080

page_access = {
    PAGE_READONLY: "r",
    PAGE_READWRITE: "rw",
    PAGE_WRITECOPY: "rwc",
    PAGE_EXECUTE: "rx",
    PAGE_EXECUTE_READ: "rx",
    PAGE_EXECUTE_READWRITE: "rwx",
    PAGE_EXECUTE_WRITECOPY: "rwxc",
}

class ProcessMemory(Processing):
    """Analyze process memory dumps."""
    def read_dump(self, filepath):
        f = open(filepath, "rb")

        while True:
            buf = f.read(24)
            if not buf:
                break

            row = struct.unpack("QIIII", buf)
            addr, size, state, typ, protect = row

            yield {
                "addr": "0x%08x" % addr,
                "end": "0x%08x" % (addr + size),
                "size": size,
                "type": typ,
                "protect": page_access.get(protect),
                "offset": f.tell(),
            }

            f.seek(size, 1)

    def create_idapy(self, process):
        i = open(process["file"], "rb")
        o = open(process["file"].replace(".dmp", ".py"), "wb")

        print>>o, "from idaapi import add_segm, mem2base, autoMark, AU_CODE"
        print>>o, "from idaapi import set_processor_type, SETPROC_ALL"
        print>>o, "set_processor_type('80386r', SETPROC_ALL)"

        for idx, region in enumerate(process["regions"]):
            i.seek(region["offset"])

            if not region["protect"]:
                section = "unk_%d" % idx
                type_ = "DATA"
            elif "x" in region["protect"]:
                section = "text_%d" % idx
                type_ = "CODE"
            elif "w" in region["protect"]:
                section = "data_%d" % idx
                type_ = "DATA"
            else:
                section = "rdata_%d" % idx
                type_ = "DATA"

            print>>o, "add_segm(0, %s, %s, '%s', '%s')" % (
                region["addr"], region["end"], section, type_
            )
            print>>o, "mem2base('%s'.decode('base64'), %s)" % (
                i.read(region["size"]).encode("base64").replace("\n", ""),
                region["addr"]
            )
            if type_ == "CODE":
                print>>o, "autoMark(%s, AU_CODE)" % region["addr"]

    def _fixup_pe_header(self, pe):
        """Fixes the PE header from an in-memory representation to an
        on-disk representation."""
        for section in pe.sections:
            section.PointerToRawData = section.VirtualAddress
            section.SizeOfRawData = max(
                section.Misc_VirtualSize, section.SizeOfRawData
            )

        reloc = pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_BASERELOC"]
        if len(pe.OPTIONAL_HEADER.DATA_DIRECTORY) < reloc:
            return

        reloc = pe.OPTIONAL_HEADER.DATA_DIRECTORY[reloc]
        if not reloc.VirtualAddress or not reloc.Size:
            return

        # Disable relocations as those have already been applied.
        reloc.VirtualAddress = reloc.Size = 0
        pe.FILE_HEADER.Characteristics |= \
            pefile.IMAGE_CHARACTERISTICS["IMAGE_FILE_RELOCS_STRIPPED"]

    def dump_images(self, process, drop_dlls=False):
        """Dump executable images from this process memory dump."""
        buf = open(process["file"], "rb").read()

        images, capture, regions, end, pe = [], False, [], None, None
        for r in process["regions"]:
            off, size = r["offset"], r["size"]

            if capture:
                if int(r["end"], 16) > end:
                    images.append((pe, regions))
                    capture = False
                else:
                    regions.append(r)
                continue

            # We're going to take a couple of assumptions for granted here.
            # Namely, the PE header is fully intact, has not been tampered
            # with, and the DOS header, the NT header, and the Optional header
            # all remain in the first page/chunk of this PE file.
            if buf[off:off+2] != "MZ":
                continue

            pe = pefile.PE(data=buf[off:off+size], fast_load=True)

            # Enable the capture of memory regions.
            capture, regions = True, [r]
            end = int(r["addr"], 16) + pe.OPTIONAL_HEADER.SizeOfImage

        # If present, also process the last loaded executable.
        if capture and regions:
            images.append((pe, regions))

        for pe, regions in images:
            img = []

            # Skip DLLs if requested to do so (the default).
            if pe.is_dll() and not drop_dlls:
                continue

            self._fixup_pe_header(pe)

            img.append(pe.write())
            for r in regions:
                img.append(buf[r["offset"]:r["offset"]+r["size"]])

            sha1 = hashlib.sha1("".join(img)).hexdigest()

            if pe.is_dll():
                filename = "%s-%s.dll_" % (process["pid"], sha1[:16])
            elif pe.is_exe():
                filename = "%s-%s.exe_" % (process["pid"], sha1[:16])
            else:
                log.warning(
                    "Unknown injected executable for pid=%s", process["pid"]
                )
                continue

            filepath = os.path.join(self.pmemory_path, filename)
            open(filepath, "wb").write("".join(img))

            yield File(filepath).get_all()

    def run(self):
        """Run analysis.

        :return: structured results.
        """
        self.key = "procmemory"
        results = []

        if self.options.get("extract_img") and not HAVE_PEFILE:
            log.warning(
                "In order to extract PE files from memory dumps it is "
                "required to have pefile installed (`pip install pefile`)."
            )

        if os.path.exists(self.pmemory_path):
            for dmp in os.listdir(self.pmemory_path):
                if not dmp.endswith(".dmp"):
                    continue

                dump_path = os.path.join(self.pmemory_path, dmp)
                dump_file = File(dump_path)

                pid, num = map(int, re.findall("(\\d+)", dmp))

                proc = dict(
                    file=dump_path, pid=pid, num=num,
                    yara=dump_file.get_yara("memory"),
                    urls=list(dump_file.get_urls()),
                    regions=list(self.read_dump(dump_path)),
                )

                if self.options.get("idapro"):
                    self.create_idapy(proc)

                if self.options.get("extract_img") and HAVE_PEFILE:
                    proc["extracted"] = list(self.dump_images(proc))

                if self.options.get("dump_delete"):
                    try:
                        os.remove(dump_path)
                    except OSError:
                        log.error("Unable to delete memory dump file at path \"%s\"", dump_path)

                results.append(proc)

        results.sort(key=lambda x: (x["pid"], x["num"]))
        return results

# Copyright (C) 2010-2013 Claudio Guarnieri.
# Copyright (C) 2014-2016 Cuckoo Foundation.
# Copyright (C) 2020-2021 PowerLZY.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os
import logging

from lib.cuckoo.core.database import Database, Task
from lib.cuckoo.common.abstracts import Processing
from lib.cuckoo.common.constants import CUCKOO_VERSION
from lib.cuckoo.common.config import emit_options
from lib.cuckoo.common.objects import File
from lib.cuckoo.common.utils import json_decode

log = logging.getLogger(__name__)

class AnalysisInfo(Processing):
    """General information about analysis session."""

    def run(self):
        """
        Run information gathering.

        :return: information dict.
        """
        self.key = "info"

        db = Database()
        dbtask = db.view_task(self.task["id"], details=True)

        if dbtask:
            task = dbtask.to_dict()
        else:
            # task is gone from the database
            if os.path.isfile(self.taskinfo_path):
                # we've got task.json, so grab info from there
                task = json_decode(open(self.taskinfo_path).read())
            else:
                # we don't have any info on the task :(
                emptytask = Task()
                emptytask.id = self.task["id"]
                task = emptytask.to_dict()

        return dict(
            version=CUCKOO_VERSION,
            started=task["started_on"],
            ended=task.get("completed_on", "none"),
            duration=task.get("duration", -1),
            id=int(task["id"]),
            category=task["category"],
            custom=task["custom"],
            owner=task["owner"],
            machine=task["guest"],
            package=task["package"],
            platform=task["platform"],
            options=emit_options(task["options"]),
            route=task["route"],
        )

class MetaInfo(Processing):
    """General information about the task and output files (memory dumps, etc)."""

    def run(self):
        """Run information gathering.

        :return: information dict.
        """
        self.key = "metadata"

        def reformat(x):
            # kinda ugly absolute -> relative
            relpath = x[len(self.analysis_path):].lstrip("/")

            dirname = os.path.dirname(relpath)
            basename = os.path.basename(relpath)
            return dict(dirname=dirname or "",
                        basename=basename,
                        sha256=File(x).get_sha256())

        meta = {
            "output": {},
        }

        if os.path.exists(self.pcap_path):
            meta["output"]["pcap"] = reformat(self.pcap_path)

        infos = [
            (self.pmemory_path, "memdumps"),
            (self.buffer_path, "buffers"),
            (self.dropped_path, "dropped"),
        ]

        for path, key in infos:
            if os.path.exists(path):
                contents = os.listdir(path)
                if contents:
                    meta["output"][key] = [reformat(os.path.join(path, i)) for i in contents]

        return meta

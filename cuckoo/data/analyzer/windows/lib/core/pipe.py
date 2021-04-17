# coding=utf-8
# Copyright (C) 2010-2013 Claudio Guarnieri.
# Copyright (C) 2014-2016 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import logging
import socket
import threading
import errno

from ctypes import create_string_buffer, c_uint, byref, sizeof

from lib.common.defines import KERNEL32, PIPE_ACCESS_INBOUND, ERROR_MORE_DATA
from lib.common.defines import PIPE_TYPE_BYTE, PIPE_WAIT, ERROR_PIPE_CONNECTED
from lib.common.defines import PIPE_UNLIMITED_INSTANCES, INVALID_HANDLE_VALUE
from lib.common.defines import FILE_FLAG_WRITE_THROUGH, PIPE_READMODE_BYTE
from lib.common.defines import ERROR_BROKEN_PIPE, PIPE_TYPE_MESSAGE
from lib.common.defines import PIPE_ACCESS_DUPLEX, PIPE_READMODE_MESSAGE

log = logging.getLogger(__name__)

BUFSIZE = 0x10000
open_handles = set()

class PipeForwarder(threading.Thread):
    """
    Forward all data received from a local pipe to the Cuckoo server through a socket.
    通过套接字将从本地管道接收到的所有数据转发到布谷鸟服务器
    """
    sockets = {}
    active = {}

    def __init__(self, pipe_handle, destination):
        threading.Thread.__init__(self)
        self.pipe_handle = pipe_handle
        self.destination = destination
        self.do_run = True

    def run(self):
        buf = create_string_buffer(BUFSIZE)
        bytes_read = c_uint()
        pid = c_uint()

        # The first four bytes indicate the process identifier. In case the
        # pipe handle is closed in an unknown way, reopening one and
        # specifying the same process identifier will reuse the same socket,
        # thus making it look like as if it was never closed in the first
        # place.
        """
        前四个字节表示进程标识符。如果管道句柄以未知的方式关闭，则重新打开一个并指定相同的进程标识符将重用同一个套接字，
        从而使其看起来就像从未关闭过一样。
        """
        success = KERNEL32.ReadFile(
            self.pipe_handle, byref(pid), sizeof(pid),
            byref(bytes_read), None
        )

        if not success or bytes_read.value != sizeof(pid):
            log.warning(
                "Unable to read the process identifier of this "
                "log pipe instance."
            )
            KERNEL32.CloseHandle(self.pipe_handle)
            return

        if self.active.get(pid.value):
            log.warning(
                "A second log pipe handler for an active process is "
                "being requested, denying request."
            )
            KERNEL32.CloseHandle(self.pipe_handle)
            return
        # 链接cuckoo主机 socket
        if pid.value:
            sock = self.sockets.get(pid.value)
            if not sock:
                sock = socket.create_connection(self.destination)
                self.sockets[pid.value] = sock

            self.active[pid.value] = True
        else:
            sock = socket.create_connection(self.destination)

        open_handles.add(sock)

        while self.do_run:
            success = KERNEL32.ReadFile(
                self.pipe_handle, byref(buf), sizeof(buf),
                byref(bytes_read), None
            )

            if success or KERNEL32.GetLastError() == ERROR_MORE_DATA:
                try:
                    # 发送 Monitor Buffer 信息
                    sock.sendall(buf.raw[:bytes_read.value])
                except socket.error as e:
                    if e.errno != errno.EBADF:
                        log.warning("Failed socket operation: %s", e)
                    break

                # If we get the broken pipe error then this pipe connection has
                # been terminated for one reason or another. So break from the
                # loop and make the socket "inactive", that is, another pipe
                # connection can in theory pick it up. (This will only happen in
                # cases where malware for some reason broke our pipe connection).
                """
                如果出现断管错误，则此管道连接因某种原因而终止.
                因此从循环中断开并使套接字处于“非活动”状态，也就是说，理论上，另一个管道连接可以拾取它.
                (这只会发生在恶意软件出于某种原因破坏我们的管道连接的情况下).
                """
            elif KERNEL32.GetLastError() == ERROR_BROKEN_PIPE:
                break
            else:
                log.warning(
                    "The log pipe handler has failed, last error %d.",
                    KERNEL32.GetLastError()
                )
                break

        if pid.value:
            self.active[pid.value] = False

    def stop(self):
        self.do_run = False

class PipeDispatcher(threading.Thread):
    """
    Receive commands through a local pipe, forward them to the dispatcher, and return the response.
    通过本地管道接收命令，将它们转发给调度程序，并返回响应
    """
    def __init__(self, pipe_handle, dispatcher):
        threading.Thread.__init__(self)
        self.pipe_handle = pipe_handle
        self.dispatcher = dispatcher
        self.do_run = True

    def _read_message(self, buf):
        """Reads a message."""
        bytes_read = c_uint()
        ret = ""

        while True:
            success = KERNEL32.ReadFile(
                self.pipe_handle, byref(buf), sizeof(buf),
                byref(bytes_read), None
            )

            if KERNEL32.GetLastError() == ERROR_MORE_DATA:
                ret += buf.raw[:bytes_read.value]
            elif success:
                return ret + buf.raw[:bytes_read.value]
            else:
                return

    def run(self):
        """Run the pipe dispatcher."""
        buf = create_string_buffer(BUFSIZE)
        bytes_written = c_uint()

        while self.do_run:
            message = self._read_message(buf)
            if not message:
                break

            response = self.dispatcher.dispatch(message) or "OK"

            KERNEL32.WriteFile(
                self.pipe_handle, response, len(response),
                byref(bytes_written), None
            )

        KERNEL32.CloseHandle(self.pipe_handle)

    def stop(self):
        self.do_run = False

class PipeServer(threading.Thread):
    """
    Accept incoming pipe handlers and initialize them in a new thread.
    接受传入的管道处理程序并在新线程中初始化它们。
    """

    def __init__(self, pipe_handler, pipe_name, message=False, **kwargs):
        threading.Thread.__init__(self)
        self.pipe_handler = pipe_handler
        self.pipe_name = pipe_name
        self.message = message
        self.kwargs = kwargs
        self.do_run = True
        self.handlers = set()

    def run(self):
        while self.do_run:
            flags = FILE_FLAG_WRITE_THROUGH
            if self.message:
                pipe_handle = KERNEL32.CreateNamedPipeA(
                    self.pipe_name, PIPE_ACCESS_DUPLEX | flags,
                    PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
                    PIPE_UNLIMITED_INSTANCES, BUFSIZE, BUFSIZE, 0, None
                )
            else:
                pipe_handle = KERNEL32.CreateNamedPipeA(
                    self.pipe_name, PIPE_ACCESS_INBOUND | flags,
                    PIPE_TYPE_BYTE | PIPE_READMODE_BYTE | PIPE_WAIT,
                    PIPE_UNLIMITED_INSTANCES, 0, BUFSIZE, 0, None
                )

            if pipe_handle == INVALID_HANDLE_VALUE:
                log.warning("Error opening logging pipe server.")
                continue

            if KERNEL32.ConnectNamedPipe(pipe_handle, None) or \
                    KERNEL32.GetLastError() == ERROR_PIPE_CONNECTED:
                handler = self.pipe_handler(pipe_handle, **self.kwargs)
                handler.daemon = True
                handler.start()
                self.handlers.add(handler)
            else:
                KERNEL32.CloseHandle(pipe_handle)

    def stop(self):
        self.do_run = False
        for h in self.handlers:
            try:
                if h.isAlive():
                    h.stop()
            except:
                pass

def disconnect_pipes():
    for sock in open_handles:
        try:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
        except:
            log.exception("Could not close socket")

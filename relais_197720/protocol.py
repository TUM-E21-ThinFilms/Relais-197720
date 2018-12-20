# Copyright (C) 2016, see AUTHORS.md
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import slave

import e21_util
from e21_util.lock import InterProcessTransportLock
from e21_util.error import CommunicationError

from slave.transport import Timeout
from slave.protocol import Protocol
from relais_197720.message import Message, Frame, Payload


class RelaisProtocol(Protocol):
    def __init__(self, logger=None):

        if logger is None:
            logger = logging.getLogger(__name__)
            logger.addHandler(logging.NullHandler())

        self.logger = logger

    def set_logger(self, logger):
        self.logger = logger

    def send_message(self, transport, message):
        message.finish()
        self.send_frame(transport, message.get_frame())

    def send_frame(self, transport, frame, retries=4):
        if retries < 0:
            raise CommunicationError("Could not send frame")

        raw_data = map(chr, frame.get_raw())

        self.logger.debug('Write (%s bytes): "%s"', str(len(raw_data)), " ".join(map(hex, frame.get_raw())))

        transport.write("".join(raw_data))

    def read_response_frame(self, transport):
        try:
            first = transport.read_bytes(4)
        except slave.transport.Timeout:
            raise CommunicationError("Received no answer")

        self.logger.debug("Received: %s", repr(first))

        try:
            while True:
                junk = transport.read_bytes(4)
        except slave.transport.Timeout:
            pass

        resp = []

        for el in first:
            resp.append(el)

        return Frame(resp)

    def read_response(self, transport):
        frame = self.read_response_frame(transport)

        if not frame.is_valid():
            self.logger.error("Received an invalid frame: %s", frame.get_raw())
            raise CommunicationError("Received an invalid frame")

        message = Message()
        message.set_frame(frame)

        return message

    def query(self, transport, message):
        with InterProcessTransportLock(transport):
            if not isinstance(message, Message):
                raise TypeError()

            self.send_message(transport, message)
            return self.read_response(transport)

    def write(self, transport, message):
        return self.query(transport, message)

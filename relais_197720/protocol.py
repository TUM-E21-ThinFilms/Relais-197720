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

from e21_util.lock import InterProcessTransportLock
from e21_util.error import CommunicationError
from relais_197720.message import Message, Frame
from serial import SerialTimeoutException


class RelayProtocol(object):
    def __init__(self, transport, logger, lock=None):
        self._transport = transport
        self._logger = logger

        if lock is None:
            lock = InterProcessTransportLock(self._transport)

        self._lock = lock

    def send_message(self, message):

        # Important, this calculates the checksum
        message.finish()

        frame = message.get_frame()
        raw_data = frame.get_raw()

        self.logger.debug('Write ({} bytes): "{}"'.format(len(raw_data), frame))

        self._transport.write(bytearray(raw_data))

    def clear(self):
        try:
            while True:
                self._transport.read_bytes(4)
        except SerialTimeoutException:
            pass

    def read_response_frames(self):
        responses = []

        try:
            while True:
                raw_data = self._transport.read_bytes(4)
                self._logger.debug("Received response '{}'".format(repr(raw_data)))
                responses.append(Frame(list(raw_data)))
        except SerialTimeoutException:
            self.clear()

        return responses

    def read_response(self):
        frames = self.read_response_frames()
        messages = []

        for frame in frames:
            if not frame.is_valid():
                self.logger.error("Received an invalid frame: {}", frame)
                raise CommunicationError("Received an invalid frame")

            message = Message()
            message.set_frame(frame)
            messages.append(message)

        return messages

    def query(self, message):
        with self._lock:
            if not isinstance(message, Message):
                raise TypeError("message is not an instance of Message")

            self.send_message(message)
            return self.read_response()

    def write(self, message):
        return self.query(message)

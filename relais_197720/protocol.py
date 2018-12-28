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
from serial import SerialTimeoutException

from e21_util.lock import InterProcessTransportLock
from e21_util.error import CommunicationError

from relais_197720.message import Message, Frame, AbstractMessage, Responses


class RelayProtocol(object):
    MESSAGE_LENGTH = 4

    def __init__(self, transport, logger):
        self._transport = transport
        self._logger = logger

    def _send_message(self, message):

        # Important, this calculates the checksum
        message.finish()

        frame = message.get_frame()
        raw_data = frame.get_raw()

        self._logger.debug('Write ({} bytes): "{}"'.format(len(raw_data), frame))

        self._transport.write(bytearray(raw_data))

    def _read_response_frames(self):
        responses = []

        try:
            while True:
                raw_data = self._transport.read_bytes(self.MESSAGE_LENGTH)
                self._logger.debug("Received response '{}'".format(repr(raw_data)))
                responses.append(Frame(list(raw_data)))
        except SerialTimeoutException:
            pass

        return responses

    def _read_response(self, msg):
        frames = self._read_response_frames()
        responses = []
        resp_class = msg.get_response_class()

        for frame in frames:
            if not frame.is_valid():
                self._logger.error("Received an invalid frame: {}", frame)
                raise CommunicationError("Received an invalid frame")

            message = Message()
            message.set_frame(frame)

            response = resp_class(message)

            # only add valid responses, and discard 'relayed messages'
            #
            # A relayed message can appear in the following case:
            #   Any cmd is sent to a non-existing relay (eg. address not existing), the
            #   cmd will be forwarded to the next relay until the last relay in the chain reads it.
            #   This relay will then just send the cmd back to the controlling pc.
            if response.is_valid():
                self._logger.debug("Got invalid response {}".format(response))
                responses.append(response)

        if len(responses) == 0:
            raise CommunicationError("Received no valid response")

        return Responses(responses)

    def query(self, message):
        # the with statement blocks all other processes/threads from accessing the transport resource,
        # well actually the device itself is blocked
        try:
            with self._transport:
                if not isinstance(message, AbstractMessage):
                    raise TypeError("message is not an instance of Message")

                self._send_message(message.get_message())
                return self._read_response(message)
        except CommunicationError as e:
            self.clear()
            raise e

    def write(self, message):
        return self.query(message)

    def clear(self):
        with self._transport:
            try:
                while True:
                    self._transport.read_bytes(self.MESSAGE_LENGTH)
            except SerialTimeoutException:
                pass

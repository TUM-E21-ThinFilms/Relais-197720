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

from serial import SerialTimeoutException

from e21_util.lock import InterProcessTransportLock
from e21_util.error import CommunicationError
from e21_util.transport import AbstractTransport

from relais_197720.message import Message, Frame, AbstractMessage, Responses


class RelayProtocol(object):
    MESSAGE_LENGTH = 4

    def __init__(self, transport, logger):
        assert isinstance(transport, AbstractTransport)
        assert isinstance(logger, logging.Logger)

        self._transport = transport
        self._logger = logger

    def _send_message(self, message):
        assert isinstance(message, Message)
        
        # Important, this calculates the checksum
        message.finish()

        frame = message.get_frame()
        raw_data = frame.get_raw()

        self._logger.debug('Write ({} bytes): "{}"'.format(len(raw_data), frame))

        self._transport.write(bytearray(raw_data))

    def _read_response_frames(self):
        responses = []

        try:
            # read as many responses as there are in the buffer. we cant know how much responses we get before hand,
            # this depends on the number of relay cards which are connected in series.
            # of course, at most 256 responses are possible
            while True:
                raw_data = self._transport.read_bytes(self.MESSAGE_LENGTH)
                self._logger.debug("Received response '{}'".format(repr(raw_data)))
                responses.append(Frame(list(raw_data)))
        except SerialTimeoutException:
            # if we have a timeout, just ignore it. actually this signals that there is no response left for
            # us to read.
            pass

        return responses

    def _read_response(self, msg):
        assert isinstance(msg, AbstractMessage)

        frames = self._read_response_frames()
        responses = []
        resp_class = msg.get_response_class()

        for frame in frames:

            # We received an invalid frame. This can mean the following:
            #   1. the relay did not produce a correct message
            #   2. we got some bit errors on the transmission process
            #
            # However, one invalid frame means that we cant trust any other frame.
            if not frame.is_valid():
                self._logger.error("Received an invalid frame: {}", frame)
                raise CommunicationError("Received an invalid frame")

            message = Message()
            message.set_frame(frame)

            # create the response from the message. the response class is derived from the message which was
            # sent to the relay card. Every message has a corresponding response.
            response = resp_class(message)

            # only add valid responses, and discard 'relayed messages'
            #
            # A relayed message can appear in the following case:
            #   Any cmd is sent to a non-existing relay (eg. address not existing), the
            #   cmd will be forwarded to the next relay until the last relay in the chain reads it.
            #   This relay will then just send the cmd back to the controlling pc.
            if response.is_valid():
                self._logger.debug(
                    "Got invalid response '{}' for response of type {}".format(response, resp_class.__name__))
                responses.append(response)

        # At least one response has to be valid. Note that not all responses are necessary valid.
        #
        #
        # Note: An invalid response is not the same as an invalid frame.
        # Invalid frame: the byte representation is not correct
        # Invalid response: We received a correct frame, but the content (e.g. command id) is unexpected or unknown.
        #
        # Consider for example the Setup message. The last response will be a relayed message, thus being invalid.
        # If we get only invalid messages, raise this exception.
        if len(responses) == 0:
            raise CommunicationError("Received no valid response")

        return Responses(responses)

    def send(self, message):
        assert isinstance(message, AbstractMessage)

        try:
            # the with statement blocks all other processes/threads from accessing the transport resource,
            # well actually the device itself is blocked
            with self._transport:

                # Send the message and return the response
                self._send_message(message.get_message())
                return self._read_response(message)
        except CommunicationError as e:
            # If we got a communication error, we should clear the serial buffer, thus
            # the next query will not run into strange problems
            self.clear()
            raise e

    def clear(self):
        with self._transport:
            try:
                # read as long as there is data still in the serial buffer
                # at some point there will be a timeout, if no data is left in the buffer
                # assuming that the timeout is not set to 0.
                while True:
                    self._transport.read_bytes(self.MESSAGE_LENGTH)
            except SerialTimeoutException:
                pass

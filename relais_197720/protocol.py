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
from slave.transport import Timeout
from slave.protocol import Protocol
from message import Message, Frame, Payload

class CommunicationError(Exception):
    pass

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

        current_frame = message.get_frame()
        self.send_frame(transport, current_frame)
            
    def send_frame(self, transport, frame, retries=4):
        if retries < 0:
            raise CommunicationError("Could not send frame")
        
        raw_data = frame.get_raw()
	raw_data = map(chr, raw_data)
        
        self.logger.debug('write (%s bytes): "%s"', str(len(raw_data)), " ".join(map(hex, frame.get_raw())))
        
        transport.write("".join(raw_data))
            
    def read_response_frame(self, transport, retries=4):
        if retries < 0:
            raise CommunicationError("Could not read response")
        
        response = []
        
        try:              
            first = transport.read_bytes(4)
        except slave.transport.Timeout:
            first = None
	
        self.logger.debug("Received: %s", repr(first))

	try:
	    # TODO: Sending `setup` cmd will probably send more than 8 bytes back 
	    # depending on the number of relais cards. currently we only support a single one.
	    # Future development could improve that?
            junk = transport.read_bytes(8)
	except slave.transport.Timeout:
            pass

	if first is None:
	    raise CommunicationError("Received no answer")

	resp = []

	for el in first:
	    resp.append(el)

	return Frame(resp)  
          
    def read_response(self, transport):

        message = Message()

        frame = self.read_response_frame(transport)
          
	if not frame.is_valid():
	    self.logger.error("Received an invalid frame: %s", frame.get_raw())
	    raise CommunicationError("Received an invalid frame")
                          
        message.set_frame(frame)
            
        return message
    
    def query(self, transport, message):
        if not isinstance(message, Message):
            raise TypeError("message must be an instance of Message")
            
        self.logger.debug('Sending message "%s"', message)
                          
        self.send_message(transport, message)
               
        response = self.read_response(transport)
        return response

    def write(self, transport, message):
        return self.query(transport, message)

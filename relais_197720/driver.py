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

from slave.driver import Driver
from protocol import RelaisProtocol
from messages.nop import NOPMessage, NOPResponse
from messages.setup import SetupMessage, SetupResponse
from messages.getport import GetPortMessage, GetPortResponse
from messages.setport import SetPortMessage, SetPortResponse
from messages.setsingle import SetSingleMessage, SetSingleResponse
from messages.delsingle import DelSingleMessage, DelSingleResponse
from messages.toggle import ToggleMessage, ToggleResponse

class RelaisDriver(Driver):
    
    RELAIS_K1 = 1
    RELAIS_K2 = 2
    RELAIS_K3 = 4
    RELAIS_K4 = 8
    RELAIS_K5 = 16
    RELAIS_K6 = 32
    RELAIS_K7 = 64
    RELAIS_K8 = 128
    
    def __init__(self, transport, protocol=None):
        if protocol is None:
            protocol = RelaisProtocol()
        
        super(RelaisDriver, self).__init__(transport, protocol)

    def send_message(self, message):
        return self._protocol.query(self._transport, message.get_message())
    
    def nop(self):
        msg = NOPMessage()
        return NOPResponse(self.send_message(msg))
    
    def setup(self):
        return SetupResponse(self.send_message(SetupMessage()))
    
    def get_port(self):
        return GetPortResponse(self.send_message(GetPortMessage()))
    
    def set_port(self, ports):
        msg = SetPortMessage()
        msg.set_port(ports)
        return SetPortResponse(self.send_message(msg))
    
    def set_single(self, ports):
        msg = SetSingleMessage()
        msg.set_single(ports)
        return SetSingleResponse(self.send_message(msg))
    
    def del_single(self, ports):
        msg = DelSingleMessage()
        msg.del_single(ports)
        return DelSingleResponse(self.send_message(msg))
    
    def toggle(self, ports):
        msg = ToggleMessage()
        msg.set_toggle(ports)
        return ToggleResponse(self.send_message(msg))

# Relais-197720, (c) 2016, see AUTHORS. Licensed under the GNU GPL.

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
        return DelSingleResponse(self.send_message(DelSingleMessage()))
    
    def toggle(self, ports):
        msg = ToggleMessage()
        msg.set_toggle(ports)
        return ToggleResponse(self.send_message(msg))
    
        
    

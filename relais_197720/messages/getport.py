# Relais-197720, (c) 2016, see AUTHORS. Licensed under the GNU GPL.

from relais_197720.message import Message, Frame, Payload, AbstractMessage, AbstractResponse

class GetPortMessage(AbstractMessage):
    def setup(self):
        payload = Payload(0)
        frame = Frame(payload)
	frame.set_payload(payload)
        frame.set_command(2)
        self.msg.set_frame(frame)
        
class GetPortResponse(AbstractResponse):
    def _is_valid(self):
        return self.msg.get_frame().get_command() == 253
    
    def get_ports(self):
        return self.msg.get_frame().get_payload().get_raw()

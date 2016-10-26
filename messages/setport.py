# Relais-197720, (c) 2016, see AUTHORS. Licensed under the GNU GPL.

from relais.message import Message, Frame, Payload, AbstractMessage, AbstractResponse

class SetPortMessage(AbstractMessage):
    def setup(self):
	self.payload = Payload(0)
        frame = Frame(self.payload)
	frame.set_payload(self.payload)
        frame.set_command(3)
        self.msg.set_frame(frame)
        
    def set_port(self, ports):
        self.payload.set_data(ports & 0xFF)
        
class SetPortResponse(AbstractResponse):
    def _is_valid(self):
        return self.msg.get_frame().get_command() == 252

# Relais-197720, (c) 2016, see AUTHORS. Licensed under the GNU GPL.

from relais_197720.message import Message, Frame, Payload, AbstractMessage, AbstractResponse

class DelSingleMessage(AbstractMessage):
    def setup(self):
        self.payload = Payload(0)
        frame = Frame(None)
	frame.set_payload(self.payload)
        frame.set_command(7)
        self.msg.set_frame(frame)
        
    def del_single(self, ports):
        self.payload.set_data(ports & 0xFF)
        
class DelSingleResponse(AbstractResponse):
    def _is_valid(self):
        return self.msg.get_frame().get_command() == 248

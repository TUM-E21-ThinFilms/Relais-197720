# Relais-197720, (c) 2016, see AUTHORS. Licensed under the GNU GPL.

from relais_197720.message import Message, Frame, Payload, AbstractMessage, AbstractResponse

class NOPMessage(AbstractMessage):
    def setup(self):
        payload = Payload(0)
        frame = Frame(payload)
        frame.set_command(0)
        self.msg.set_frame(frame)
        
class NOPResponse(AbstractResponse):
    def _is_valid(self):
        return self.msg.get_frame().get_command() == 255

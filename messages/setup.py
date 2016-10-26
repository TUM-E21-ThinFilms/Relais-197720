# Relais-197720, (c) 2016, see AUTHORS. Licensed under the GNU GPL.

from relais.message import Message, Frame, Payload, AbstractMessage, AbstractResponse

class SetupMessage(AbstractMessage):
    def setup(self):
        payload = Payload(0)
        frame = Frame(payload)
        frame.set_command(1)
        self.msg.set_frame(frame)
        
class SetupResponse(AbstractResponse):
    def _is_valid(self):
        return self.msg.get_frame().get_command() == 254
    
    def get_version(self):
        return self.msg.get_frame().get_payload().get_raw()

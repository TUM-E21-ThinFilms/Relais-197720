# Relais-197720, (c) 2016, see AUTHORS. Licensed under the GNU GPL.


class Message(object):    
    def __init__(self):
        self.frame = None
        
    def get_frame(self):
        return self.frame
        
    def set_frame(self, frame):
        if not isinstance(frame, Frame):
            raise TypeError()
        
        self.frame = frame

    def finish(self):        
        self.frame.set_checksum(self.frame.compute_checksum())
            
    def __str__(self):
        return str(self.frame)

class Payload(object):
    def __init__(self, raw_payload):
	self.data = 0

	if not raw_payload is None:
            self.data = raw_payload & 0xFF
        
    def set_data(self, data):
        self.data = data & 0xFF
        
    def get_data(self):
        return self.data
    
    def get_raw(self):
        return self.data
    
class Frame(object):
    
    def __init__(self, raw_frame=None): 
        if isinstance(raw_frame, list) and len(raw_frame) == 4:
            self.set_command(raw_frame[0])
            self.set_address(raw_frame[1])
            self.payload = Payload(raw_frame[2])
            self.chksum = raw_frame[3] & 0xFF       
        else:
            self.cmd = 0
            self.addr = 1
            self.payload = Payload(None)
            self.chksum = 0
        
    def set_command(self, cmd):
        self.cmd = cmd & 0xFF
        
    def get_command(self):
        return self.cmd
    
    def set_address(self, addr):
        self.addr = addr & 0xFF
        
    def get_address(self):
        return self.addr
    
    def set_checksum(self, chksum):
        self.chksum = chksum & 0xFF
        
    def get_checksum(self):
        return self.chksum
        
    def is_valid(self):        
        return self.get_checksum() == self.compute_checksum()
        
    def compute_checksum(self):
        array = [self.cmd, self.addr, self.payload.get_raw()]
        
        chksum = 0
        for data in array:
            chksum = chksum ^ data
           
        return chksum
    
    def set_payload(self, payload):
        if not isinstance(payload, Payload):
            raise TypeError()
        
        self.payload = payload
        
    def get_payload(self):
        return self.payload
    
    def get_raw(self):
        return [self.cmd, self.addr, self.payload.get_raw(), self.chksum]
        
class AbstractMessage(object):
    def __init__(self):
        self.msg = Message()
	self.payload = None
	self.frame = None
        self.setup()
        
    def get_message(self):
        return self.msg
    
    def setup(self):
        raise NotImplementedError()
    
class AbstractResponse(object):
    def __init__(self, message):
        if not isinstance(message, Message):
	    raise TypeError()
        
	self.msg = message
    
    def get_response(self):

        return self.msg
    
    def is_valid(self):
        return self.msg.is_valid() and self._is_valid()
        
    def _is_valid(self):
        return True

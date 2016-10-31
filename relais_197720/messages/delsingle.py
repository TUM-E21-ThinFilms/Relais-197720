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

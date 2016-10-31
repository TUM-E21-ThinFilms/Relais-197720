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

from relais.message import Message, Frame, Payload, AbstractMessage, AbstractResponse

class NOPMessage(AbstractMessage):
    def setup(self):
        payload = Payload(0)
        frame = Frame(payload)
        frame.set_command(0)
        self.msg.set_frame(frame)
        
class NOPResponse(AbstractResponse):
    def _is_valid(self):
        return self.msg.get_frame().get_command() == 255

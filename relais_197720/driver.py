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

from relais_197720.protocol import RelayProtocol
from relais_197720.messages.nop import NOPMessage, NOPResponse
from relais_197720.messages.setup import SetupMessage, SetupResponse
from relais_197720.messages.getport import GetPortMessage, GetPortResponse
from relais_197720.messages.setport import SetPortMessage, SetPortResponse
from relais_197720.messages.setsingle import SetSingleMessage, SetSingleResponse
from relais_197720.messages.delsingle import DelSingleMessage, DelSingleResponse
from relais_197720.messages.toggle import ToggleMessage, ToggleResponse


class RelayDriver(object):

    def __init__(self, protocol):
        self._protocol = protocol

    def send_message(self, message, address):
        message.get_message().get_frame().set_address(address)
        return self._protocol.query(message.get_message())

    def nop(self, address):
        msg = NOPMessage()
        return NOPResponse(self.send_message(msg, address))

    def setup(self, address=1):
        return SetupResponse(self.send_message(SetupMessage(), address))

    def get_port(self, address):
        return GetPortResponse(self.send_message(GetPortMessage(), address))

    def set_port(self, ports, address):
        msg = SetPortMessage()
        msg.set_port(ports)
        return SetPortResponse(self.send_message(msg, address))

    def set_single(self, ports, address):
        msg = SetSingleMessage()
        msg.set_single(ports)
        return SetSingleResponse(self.send_message(msg, address))

    def del_single(self, ports, address):
        msg = DelSingleMessage()
        msg.del_single(ports)
        return DelSingleResponse(self.send_message(msg, address))

    def toggle(self, ports, address):
        msg = ToggleMessage()
        msg.set_toggle(ports)
        return ToggleResponse(self.send_message(msg, address))

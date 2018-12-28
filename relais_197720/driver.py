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
from relais_197720.messages.nop import NOPMessage
from relais_197720.messages.setup import SetupMessage
from relais_197720.messages.getport import GetPortMessage
from relais_197720.messages.setport import SetPortMessage
from relais_197720.messages.setsingle import SetSingleMessage
from relais_197720.messages.delsingle import DelSingleMessage
from relais_197720.messages.toggle import ToggleMessage


class RelayDriver(object):

    def __init__(self, protocol):
        self._protocol = protocol

    def send_message(self, message, address):
        message.get_message().get_frame().set_address(address)
        return self._protocol.query(message)

    def nop(self, address):
        msg = NOPMessage()
        return self.send_message(msg, address)

    def setup(self, address=1):
        return self.send_message(SetupMessage(), address)

    def get_port(self, address):
        return self.send_message(GetPortMessage(), address)

    def set_port(self, address, ports):
        msg = SetPortMessage()
        msg.set_port(ports)
        return self.send_message(msg, address)

    def set_single(self, address, ports):
        msg = SetSingleMessage()
        msg.set_single(ports)
        return self.send_message(msg, address)

    def del_single(self, address, ports):
        msg = DelSingleMessage()
        msg.del_single(ports)
        return self.send_message(msg, address)

    def toggle(self, address, ports):
        msg = ToggleMessage()
        msg.set_toggle(ports)
        return self.send_message(msg, address)

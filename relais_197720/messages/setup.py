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


class SetupMessage(AbstractMessage):
    def setup(self):
        self.frame.set_command(1)


class SetupResponse(AbstractResponse):
    def _is_valid(self):
        return all(map(lambda x: x.get_frame().get_command() == 254, self.msg))

    def get_version(self):
        return self.msg.get_frame().get_payload().get_raw()

    def get_number_of_devices(self):
        # Every relay card generates after receiving the setup cmd a response, containing
        # an increased address. Hence, for three relay cards, the following messages are sent:
        #  relay-card 1:
        #       resp(addr=0x01), cmd(setup, addr=0x02) -> cmd intercepted by relay 2
        #  relay-card 2:
        #       resp(addr=0x02), cmd(setup, addr=0x03) -> cmd intercepted by relay 3
        #  relay-card 3:
        #       resp(addr=0x03), cmd(setup, addr=0x04) -> cmd not intercepted, hence sent back to control pc
        #
        # Hence, in total N + 1 messages are sent back to the control pc.
        return len(self.msgs) - 1


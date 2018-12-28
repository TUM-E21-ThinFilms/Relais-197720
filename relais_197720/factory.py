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
from relais_197720.driver import RelayDriver
from e21_util.pvd.transport import Serial
from e21_util.log import get_logger
from e21_util.ports import Ports


class RelayFactory(object):

    def get_logger(self):
        return get_logger('Relay-197720', 'relay.log')

    def create_relay(self, device=None, logger=None):
        if logger is None:
            logger = self.get_logger()

        if device is None:
            device = Ports().get_port(Ports.DEVICE_RELAY)

        transport = Serial(device, 19200, 8, 'N', 1, 1)

        return RelayDriver(RelayProtocol(transport, logger=logger))

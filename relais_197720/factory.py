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

from protocol import RelaisProtocol
from driver import RelaisDriver
from e21_util.transport import Serial
from e21_util.logging import get_sputter_logger

class RelaisFactory:
	
	def get_logger(self):
		return get_sputter_logger('Relais-197720', 'relais.log')

	def create_relais(self, device='/dev/ttyUSB3', logger=None):
		if logger is None:
			logger = self.get_logger()

		return RelaisDriver(Serial(device, 19200, 8, 'N', 1, 1), RelaisProtocol(logger=logger))

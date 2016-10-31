# Relais-197720, (c) 2016, see AUTHORS. Licensed under the GNU GPL.

from protocol import RelaisProtocol
from driver import RelaisDriver
from slave.transport import Serial
import logging

class RelaisFactory:
	
    def get_logger(self):
	logger = logging.getLogger('Relais-197720')
	logger.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh = logging.FileHandler('relais.log')
	fh.setLevel(logging.DEBUG)
	fh.setFormatter(formatter)
	logger.addHandler(fh)
	return logger

    def create_relais(self, device='/dev/ttyUSB3', logger=None):
	# use your own device mapping here...
	if logger is None:
	    logger = self.get_logger()

        return RelaisDriver(Serial(device, 19200, 8, 'N', 1, 1), RelaisProtocol(logger=logger))

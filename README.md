# Relais-197720
Serial RS232 python implementation of the "Conrad 197720 Relaiskarte"

See https://www.conrad.de/de/relaiskarte-baustein-197720-12-vdc-24-vdc-197720.html

Usage
-----

#### Listen on device /dev/ttyUSB2
```
import logging

from relais_197720.factory import *
from e21_util.serial_connection import *

# Configure your serial port here
serial = Serial('/dev/ttyUSB2')

# Configure your logger if you need one
logger = logging.getLogger('relay')

relay = RelayFactory.create(serial, logger)
```

#### Setup relais cards (up to 255 in series)
```
relais.setup()
```

#### Test message
```
relais.nop() # NoOperation
```

#### Reading active ports
```
ports = relais.get_port()
if ports.get_ports() & 16:
    print("port 5 active") # 5^2 = 16
```
#### Setting ports
```
relais.set_port(255) # Enable all ports
relais.set_port(1 + pow(2,2) + pow(2,6)) # Enabled port 1,2 and 6, disable all other
```

#### Set/del/toggle single port
```
relais.set_single(8) # enable port 4
relais.del_single(64) # disable port 7
relais.toggle(8 + 64) # toggle port 4 and 7
``` 

Installation
-----------
To install, simply do
```
python setup.py install
```


Requirements
------------

- Python 2.6 or higher
- slave 0.4.0 or higher (https://github.com/p3trus/slave)

Licensing
---------

You should have received a copy of the `GNU General Public License` along with Relais-197720; see the file COPYING

GNU General Public License: http://www.gnu.org/licenses/gpl.html

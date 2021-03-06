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
from e21_util.hinting import List

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
            self.payload, self.chksum = Payload(raw_frame[2]), raw_frame[3] & 0xFF
        else:
            self.cmd, self.addr, self.payload, self.chksum = 0, 1, Payload(None), 0

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

        chksum = 0
        for data in [self.cmd, self.addr, self.payload.get_raw()]:
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

    def __str__(self):
        return " ".join(map(hex, self.get_raw()))


class AbstractMessage(object):
    def __init__(self):
        self.payload, self.frame, self.msg = Payload(None), Frame(None), Message()
        self.frame.set_payload(self.payload)
        self.msg.set_frame(self.frame)
        self.setup()

    def get_message(self):
        return self.msg

    def setup(self):
        raise NotImplementedError()

    def get_response_class(self):
        raise NotImplementedError()


class AbstractResponse(object):
    def __init__(self, message):
        assert isinstance(message, Message)

        self.msg = message

    def get_address(self):
        return self.msg.get_frame().get_address()

    def get_response(self):
        return self.msg

    def is_valid(self):
        return self._is_valid()

    def _is_valid(self):
        return True

    def __str__(self):
        return str(self.msg)


class Responses(object):
    def __init__(self, responses):
        assert List(AbstractResponse) == responses
        self._resps = responses

    def get_number(self):
        return len(self._resps)

    def get_response(self):
        if len(self._resps) > 0:
            return self._resps[0]

        # should not happen
        raise RuntimeError("Received no responses, protocol should have raised an exception beforehand")

    def get_responses(self):
        return self._resps

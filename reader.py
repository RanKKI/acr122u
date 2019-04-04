from smartcard.System import readers
from smartcard.util import toHexString

from errors import AuthenticationException, NoCardException, NoReaderException


class AcrReader(object):

    locked = True

    def __init__(self):
        r = readers()
        if len(r) == 0:
            raise NoReaderException()
        self.reader = r[0]
        self.con = self.reader.createConnection()

    def excute(self, cmd):
        data, sw1, sw2 = self.con.transmit(cmd)
        if (sw1, sw2) == (0x90, 0x0):
            return data
        print("Error", data, sw1, sw2)

    def _divide_value(self, value: str) -> list:
        return [value[i]+value[i+1] for i in range(0, len(value), 2)]

    def _load_auth_key(self, key: str, pos=0x00) -> bool:
        cmd = [0xFF, 0x82, 0x00, pos, 0x06]
        cmd.extend(self._divide_value(key))
        return self.excute(cmd) is not None

    def load(self, args):
        if self._load_auth_key(list(map(lambda x: int(x, 16), args[0]))):
            print("succeed loaded auth key")

    def _authentication(self, sector, key_type=0x60, pos=0x00) -> bool:
        cmd = [0xFF, 0x86, 0x00, 0x00, 0x05,
               0x01, 0x00, sector*4, key_type, pos]
        return self.excute(cmd) is not None

    def authentication(self, sector) -> bool:
        return self._authentication(sector) or self._authentication(sector, key_type=0x61)

    def _read_block(self, block: int):
        cmd = [0xFF, 0xB0, 0x00, block, 0x10]
        data = self.excute(cmd)
        if not data:
            return None
        return f"Block {str(block).rjust(2)}: {toHexString(data)}"

    def _read_sector(self, sector):
        if not self.authentication(sector):
            raise AuthenticationException()
        print("-"*24 + f"Sector {str(sector).rjust(2)}" + "-"*24)
        data = []
        for block in range(sector*4, (sector+1)*4):
            values = self._read_block(block)
            print(values)
            data.append(values)
        return data

    def read(self, sectors=None, block=None):
        if isinstance(sectors, str) and "-" in sectors:
            start, end = sectors.split("-")
            sectors = range(start, end+1)
        elif isinstance(sectors, int):
            sectors = [sectors]
        elif block:
            sectors = [int(block / 4)]
        elif not sectors:
            sectors = range(0, 16)

        for sector in sectors:
            self._read_sector(sector)
        print("-"*57)

    def dump(self, file="./output.dump"):
        with open(file, "w") as f:
            for sector in range(0, 15):
                for block in self._read_sector(sector):
                    f.write(f"{block}\n")
                f.write(f"{'-'*57}\n")

    def _write_block(self, block: int, values: str):
        sector = int(block / 4)
        if not self.authentication(sector):
            raise AuthenticationException()
        value_data = list(map(lambda x: int(x, 16), values))    

        cmd = [0xFF, 0xD6, 0x00, block, 0x10]
        cmd.extend(value_data)

        if self.excute(cmd) is not None:
            print(f"Wrote {' '.join(values)} to block {block} sucessed")
            print("Current sector status")
            self._read_sector(sector)

    def write(self, block: int, value):
        value = value.replace(" ", "").ljust(32, "0")
        self._write_block(block, self._divide_value(value))


if __name__ == "__main__":
    sr = AcrReader()
    sr.con.connect()

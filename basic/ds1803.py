from machine import I2C, Pin


class DS1803():
    CONTROL_WRITE = 0x50
    CONTROL_READ = 0x51
    COMMAND_BOTH = 0xAF
    COMMAND_POT_0 = 0XA9
    COMMAND_POT_1 = 0XAA

    def __init__(self):
        # HW i2c
        self.i2c = I2C(1,sda=Pin(21), scl=Pin(22), freq=400000)
        self.address =  self.__get_i2c_address()

    def __get_i2c_address(self) -> int:
        addresses = self.i2c.scan()
        if len(addresses) > 0:
            addrs = addresses[0]
            print(f'Using address {addrs}')
            return addrs

    def _set_value(self, value:int, command_byte=None):
        if not command_byte:
            command_byte = self.COMMAND_BOTH
        self.i2c.writeto(self.address, bytes([self.CONTROL_WRITE]))
        self.i2c.writeto(self.address, bytes([command_byte, value]))

    def set_pot0_value(self, value: int):
        self._set_value(value, self.COMMAND_POT_0)

    def set_pot1_value(self, value: int):
        self._set_value(value, self.COMMAND_POT_1)

    def get_values(self):
        read_response = bytearray(2)
        self.i2c.writeto(self.address, bytes([self.CONTROL_READ]))
        # 1 byte for each pot
        self.i2c.readfrom_into(self.address, read_response)
        return (read_response[0], read_response[1])

    def get_pot0_value(self):
        return self.get_values()[0]

    def get_pot1_value(self):
        return self.get_values()[1]

    def reset_pots(self):
        """
        Set both potentiometers to 0. H-W -> 10kO
        """
        self._set_value(0)


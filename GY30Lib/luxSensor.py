#!/usr/bin/env python

import smbus

class GY30:
    __bus = smbus.SMBus(0)
    __addr = 0x00

    def __init__(self, bus, addr):
        self.__bus = bus
        self.__addr = addr
        # when read data at first, return always zero.
        bus.read_i2c_block_data(self.__addr,0x11)

    def read(self):
        luxRead = self.__bus.read_i2c_block_data(self.__addr,0x11)
        return luxRead[1]* 10

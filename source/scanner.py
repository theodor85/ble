from time import sleep

from bluepy.btle import Scanner, ScanEntry


class MyScanEntry:

    def __init__(self, addr, addrType, rssi):
        self._addr = addr
        self._addrType = addrType
        self._rssi = rssi

    @property
    def addr(self):
        return self._addr

    @property
    def addrType(self):
        return self._addrType
    
    @property
    def rssi(self):
        return self._rssi


def my_scan(timeout):
    sleep(timeout)
    return [
        ScanEntry('12345', 'ADDR_TYPE_PUBLIC', -25),
        ScanEntry('54321', 'ADDR_TYPE_PUBLIC', -50),
    ]


TEST_DATA = [
    [51, 51], # 1
    [63, 45], # 2
    [76, 42], # 3
    [89, 45], # 4
    [86, 58], # 5
    [84, 72], # 6
    [86, 86], # 7
    [89, 100], # 8
    [76, 99], # 9
    [67, 92], # 10
    [64, 78], # 11
    [64, 64], # 12
    [50, 67], # 13
    [45, 63], # 14
]

def scan(timeout):
    scanner = Scanner()
    scanner.scan = my_scan
    return scanner.scan(timeout)

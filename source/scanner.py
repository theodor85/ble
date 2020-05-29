from time import sleep
from random import randint

from bluepy.btle import Scanner, ScanEntry


class MyScanEntry:
    ''' Класс-заглушка, заменяющий bluepy.btle.ScanEntry '''

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


TEST_DATA = [
    [-44.15, -44.15],
    [-45.98, -43.06],
    [-47.61, -42.46],
    [-48.98, -43.06],
    [-48.68, -45.26],
    [-48.48, -47.14],
    [-48.68, -48.68],
    [48.98, -50.0],
    [-47.61, -49.91],
    [-46.52, -49.27],
    [-46.12, -47.84],
    [-46.12, -46.12],
    [-43.97, -46.52],
    [-43.06, -45.98],
]

def my_scan(anchor, timeout):
    ''' Функция, имитирующая нахождение точек (устройств) '''

    sleep(timeout)
    result = list()

    # точка 1
    elem = TEST_DATA[randint(0, 13)]
    if anchor=='anchor1':
        signal_level_dBm = elem[0]
    else:
        signal_level_dBm = elem[1]
    result.append(MyScanEntry('12345', 'ADDR_TYPE_PUBLIC', signal_level_dBm))

    # точка 2
    elem = TEST_DATA[randint(0, 13)]
    if anchor=='anchor1':
        signal_level_dBm = elem[0]
    else:
        signal_level_dBm = elem[1]
    result.append(MyScanEntry('54321', 'ADDR_TYPE_PUBLIC', signal_level_dBm))

    # точка 3
    elem = TEST_DATA[randint(0, 13)]
    if anchor=='anchor1':
        signal_level_dBm = elem[0]
    else:
        signal_level_dBm = elem[1]
    result.append(MyScanEntry('3698', 'ADDR_TYPE_PUBLIC', signal_level_dBm))

    return result

def scan_anchor(anchor, timeout):
    ''' Запускается сканирование устройств
    '''

    if anchor=='anchor1':
        index=0
    elif anchor=='anchor2':
        index=1

    scanner = Scanner(index)
    scanner.scan = my_scan  # здесь делаем заглушку на функцию с тестовыми данными
    return scanner.scan(anchor, timeout)

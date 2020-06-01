''' В модуле определены функции для сканирования устройств и получения
    данных о них: адрес, тип адреса, уровинь сигнала (RSSI).
    
    В данный момент функция сканирования заменена заглушкой, 
    используются тестовые уровни сигналов в TEST_DATA.
'''

from time import sleep
from random import randint

from bluepy.btle import Scanner


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
    [-75.06, -45.98],
]

def my_scan(timeout):
    ''' Функция, имитирующая нахождение точек (устройств) '''

    sleep(timeout)
    result = list()

    # точка 1
    elem = TEST_DATA[randint(0, len(TEST_DATA)-1)]
    signal_level_dBm = elem[0]
    result.append(MyScanEntry('12345', 'ADDR_TYPE_PUBLIC', signal_level_dBm))

    # точка 2
    elem = TEST_DATA[randint(0, len(TEST_DATA)-1)]
    signal_level_dBm = elem[0]
    result.append(MyScanEntry('54321', 'ADDR_TYPE_PUBLIC', signal_level_dBm))

    # точка 3
    elem = TEST_DATA[randint(0, len(TEST_DATA)-1)]
    signal_level_dBm = elem[0]
    result.append(MyScanEntry('3698', 'ADDR_TYPE_PUBLIC', signal_level_dBm))

    return result

def scan_anchor(timeout):
    ''' Запускается сканирование устройств
    '''

    scanner = Scanner()
    scanner.scan = my_scan  # здесь делаем заглушку на функцию с тестовыми данными
    return scanner.scan(timeout)

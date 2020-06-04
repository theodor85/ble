''' В модуле определены функции для сканирования устройств и получения
    данных о них: адрес, тип адреса, уровинь сигнала (RSSI).
    
'''

from bluepy.btle import Scanner


def scan_anchor(timeout):
    ''' Запускается сканирование устройств
    '''

    scanner = Scanner()
    return scanner.scan(timeout)

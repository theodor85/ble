''' Модуль содержит функции для нахождения расстояния до меток
    по уровню сигнала
'''
from math import pow

def convert_dB_to_m(dB_level):
    
    # для простоты возьмем формулу отсюда:
    # https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D0%B5%D0%BB%D1%8C_%D1%83%D1%80%D0%BE%D0%B2%D0%BD%D1%8F_%D0%BF%D1%80%D0%B8%D0%BD%D0%B8%D0%BC%D0%B0%D0%B5%D0%BC%D0%BE%D0%B3%D0%BE_%D1%81%D0%B8%D0%B3%D0%BD%D0%B0%D0%BB%D0%B0
    
    # предположим, что уровень сигнала на расстоянии 1 м будет 10 дБм:
    P0 = -10  # его нужно измерять экспериментально, дБм
    d0 = 1    # контрольное расстояние - 1 м
    n = 2     # коэффициент потерь мощности сигнала при распространении в среде,
              # для воздуха равен 2
    
    Pd = dB_level   # измеренное значение, дБм
    
    temp = (P0 - Pd) / (10 * n)
    d = d0 * pow(10, temp)
    return d

def convert_from_dB_to_meters(devices_list):
    ''' Функция вычисляет расстояние, исходя из уровня сигнала
    '''

    result = list()
    for dev in devices_list:
        addr = dev.addr
        dB_level = dev.rssi
        meters = round(convert_dB_to_m(dB_level))
        result.append([addr, meters])

    return result

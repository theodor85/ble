from math import sqrt, pow


X = 100
Y = 100


def convert_dB_to_m(dB_level):
    
    # для простоты возьмем формулу отсюда:
    # https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D0%B5%D0%BB%D1%8C_%D1%83%D1%80%D0%BE%D0%B2%D0%BD%D1%8F_%D0%BF%D1%80%D0%B8%D0%BD%D0%B8%D0%BC%D0%B0%D0%B5%D0%BC%D0%BE%D0%B3%D0%BE_%D1%81%D0%B8%D0%B3%D0%BD%D0%B0%D0%BB%D0%B0

    # предположим, что уровень сигнала на расстоянии 1 м будет 10 дБм:
    P0 = -20  # его нужно измерять экспериментально, дБм
    d0 = 1    # контрольное расстояние - 1 м
    n = 3     # коэффициент потерь мощности сигнала при распространении в среде,
              # для воздуха равен 2

    Pd = dB_level   # измеренное значение, дБм
    print(f'*****Pd = {Pd}')

    temp = (P0 - Pd) / (10 * n)
    print(f'*****temp = {temp}')
    d = d0 * pow(10, temp)
    print(f'*****d = {d}')
    return d


def get_device_coords(signal_anchor1, signal_anchor2):
    ''' Функция на вход получает уровни сигналов от устройств.
        Возвращает координаты, полученные через теорему косинусов
    '''
    print(signal_anchor1)
    print(signal_anchor2)

    r1 = convert_dB_to_m(signal_anchor1)
    r2 = convert_dB_to_m(signal_anchor2)

    print(r1)
    print(r2)
    
    x = X - (pow(X, 2)+pow(r2, 2)-pow(r1, 2)) / (2 * X)
    x = round(x)

    temp = (pow(X, 2)+pow(r2, 2)-pow(r1, 2)) / (2*X*r2)
    temp = 1 - pow(temp, 2)

    if temp < 0:
        temp = -temp

    h = r2 * sqrt( temp )
    y = Y - h
    print(y)
    y = round(y)

    return x, y

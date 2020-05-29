''' В модуле определены функции для работы с параметрами
    запретной зоны. Также определен класс Config, хранящий 
    параметры, загруженные из конфигурационного файла.
'''

CONFIG_FILE_PATH = 'config.conf'


def is_restricted_area_violation(x, y):
    ''' Возвращает True, если точка попадает в запретную зону.
        Иначе - False
    '''
    try:
        restr_area_size = int(Config().restricted_area)
    except AttributeError:
        # запретная зона не определена, всегда False
        return False

    if y < restr_area_size:
        return True
    else:
        return False

def get_restricted_area_size():
    try:
        restr_area_size = int(Config().restricted_area)
    except AttributeError:
        # запретная зона не определена
        return 0
    return restr_area_size


class Config:
    ''' Класс хранит параметры конфигурации.
        Построен как Singleton
    '''
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        # загрузка из файла
        with open(CONFIG_FILE_PATH, 'r') as conf_file:
            for line in conf_file:
                key = line.split('=')[0].strip()
                value = line.split('=')[1].strip()
                self.__dict__[key] = value

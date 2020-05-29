

CONFIG_FILE_PATH = 'config.conf'


def check_restricted_area(x, y):
    ''' Возвращает False, если точка попадает в запретную зону.
        Иначе - True
    '''
    try:
        restr_area_size = Config().restricted_area
    except AttributeError:
        # запретная зона не определена, всегда True
        return True

    if y < restr_area_size:
        return False
    else:
        return True

def get_restricted_area_size():
    try:
        restr_area_size = Config().restricted_area
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

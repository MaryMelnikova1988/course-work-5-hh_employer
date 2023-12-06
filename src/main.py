from pprint import pprint

from src.config import config
from src.utils import get_hh_data, create_database, save_data_to_database


def main():
    db_name = 'hh'
    employer_ids = [
        1740,  # яндекс
        2180,  # озон
        67611,  # тензор
        3529,  # сбер
        4181,  # втб
        6591,  # псб
        1455,  # hh
        15478,  # vk
        64174,  # 2ГИС
        3713346,  # ЯНОС
        #     '5060211#main'  # ГК АСтра
    ]
    params = config()
    data = get_hh_data(employer_ids)
    # pprint(data)
    create_database(db_name, params)
    save_data_to_database(data, db_name, params)


if __name__ == '__main__':
    main()

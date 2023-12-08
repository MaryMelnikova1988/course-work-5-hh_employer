from pprint import pprint

from src.config import config
from src.utils import *
from src.class_DBManager import DBManager


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
    employers = get_hh_employers(employer_ids)
    # pprint(employers)
    # pprint(len(employers))
    vacancies = get_hh_vacancies(employer_ids)
    # pprint(vacancies)
    # pprint(len(vacancies))
    # save_data_to_database(data, db_name, params)

    # create_database(db_name, params)
    # save_employers_to_database(employers,db_name,params)
    # save_vacancies_to_database(vacancies,db_name, params)
    DBManager.get_companies_and_vacancies_count()



if __name__ == '__main__':
    main()


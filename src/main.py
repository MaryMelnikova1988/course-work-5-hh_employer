from src.class_DBManager import DBManager
from src.config import config
from src.utils import *


def main():
    # исходные данные
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
    # получение данныx о работодателях и их вакансиях с API hh.ru
    employers = get_hh_employers(employer_ids)
    vacancies = get_hh_vacancies(employer_ids)
    # Создание и сохранение БД PostgreSQL
    create_database(db_name, params)
    print(f"БД {db_name} успешно создана")
    save_employers_to_database(employers, db_name, params)
    save_vacancies_to_database(vacancies, db_name, params)
    print(f"В БД {db_name} успешно добавлены данные о работодателях и их вакансиях")
    print("Обратите внимание,в базе данных могут отсутствовать строки, если зарплата работодателями не указана")
    # работа с БД PostgreSQL
    database= DBManager()
    database.get_companies_and_vacancies_count()
    # database.get_all_vacancies()
    # database.get_avg_salary()
    # database.get_avg_salary_for_vacancy()

    #
    # DBManager.get_companies_and_vacancies_count()
    # DBManager.get_all_vacancies()
    # DBManager.get_avg_salary()
    # DBManager.get_avg_salary_for_vacancy()
    # DBManager.get_vacancies_with_higher_salary()
    # print("""Пользователь сейчас будем получать список всех вакансий, в названии которых содержатся переданные в метод слова, например разработчик.
    # Введите, требуемое слово для поиска: """)
    # keyword =input().lower()
    # DBManager.get_vacancies_with_keyword(keyword)
    # database.get_vacancies_with_keyword()


if __name__ == '__main__':
    print("""Здравствуйте, пользователь.
    Поможем получить информацию о работодателях и их вакансиях в России от 10 интересных компаний:
    Яндекс, Ozon, Тензор, СБЕР, Банк ВТБ (ПАО),ПСБ (ПАО «Промсвязьбанк»), HeadHunter, VK, 2ГИС, Славнефть-ЯНОС.
    Процесс пошел, оставайтесь с нами""")
    main()
    print("Данные получены. До скорых новых встреч.")

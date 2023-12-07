from pprint import pprint
from prettytable import PrettyTable
from src.config import config

import psycopg2


class DBManager:
    """Класс, который будет подключаться к БД PostgreSQL"""

    def __init__(self, db_name, params=config()):
        self.db_name = db_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """Получение списка всех компаний и количество вакансий у каждой компании"""
        # conn = psycopg2.connect(database=self.db_name, **self.params)
        conn = psycopg2.connect(
            host="localhost",
            database="hh",
            user="postgres",
            password="721719"
        )
        with conn.cursor() as cur:
            cur.execute("""
                  select employer_name, employer_open_vacancies from employers
                      """)
            rows = cur.fetchall()
            table=PrettyTable()
            table.field_names=["employer_name", "employer_open_vacancies"]
            table.add_rows(rows)
            print(table)
            # pprint(rows)
            # data = "\n".join([str(row) for row in rows])
            # print(data)

        conn.commit()
        conn.close()

    def get_all_vacancies(self):
        """Получение списка всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        pass

    def get_avg_salary(self):
        """Получение средней зарплаты по вакансиям"""
        pass

    def get_vacancies_with_higher_salary(self):
        """ Получение списка всех вакансий,
        у которых зарплата выше средней по всем вакансиям"""
        pass

    def get_vacancies_with_keyword(self):
        """Получение списка всех вакансий,
         в названии которых содержатся переданные в метод слова,
          например python"""
        pass

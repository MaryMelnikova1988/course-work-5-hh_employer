import psycopg2
from prettytable import PrettyTable


class DBManager:
    """Класс, который будет подключаться к БД PostgreSQL"""

    # conn = psycopg2.connect(
    #     host="localhost",
    #     database='hh',
    #     user="postgres",
    #     password="721719"
    # )
    # def __init__(self, dbname: str = 'hh', user: str = "postgres", password: str = "721719", host: str = 'localhost', port: str = '5432'):
    #     self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    #     self.cur = self.conn.cursor()
    @classmethod
    def get_conn(cls):
        return psycopg2.connect(
        host="localhost",
        database='hh',
        user="postgres",
        password="721719"
    )

    def get_companies_and_vacancies_count(self):
        """Получение списка всех компаний и количество вакансий у каждой компании"""
        # with self.conn:
        #     self.cur.execute
        conn = self.get_conn()
        with conn.cursor() as cur:
            cur.execute("""
                  SELECT employer_name, employer_open_vacancies FROM employers
                      """)
            rows = cur.fetchall()
            table = PrettyTable()
            table.field_names = ["название компании (работодателя)", "количество открытых вакансий у компании"]
            table.add_rows(rows)
            print(table)

        conn.commit()
        conn.close()



    def get_all_vacancies(self):
        """Получение списка всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        self.conn
        with self.conn.cursor() as cur:
            cur.execute("""
                     SELECT employers.employer_name, vacancy_name, vacancy_salary, vacancy_url FROM vacancies
JOIN employers USING(employer_id)
                          """)
            rows = cur.fetchall()
            table = PrettyTable()
            table.field_names = ["название компании (работодателя)", "название вакансии", "зарплата, руб",
                                 "ссылка на вакансию"]
            table.add_rows(rows)
            print(table)

        self.conn.commit()
        self.conn.close()

    def get_avg_salary(self):
        """Получение средней зарплаты по вакансиям"""
        self.conn
        with self.conn.cursor() as cur:
            cur.execute("""
                             SELECT AVG(vacancy_salary) FROM vacancies
                                  """)
            rows = cur.fetchall()
            table = PrettyTable()
            table.field_names = ["средняя ЗП по всем вакансиям и всем работодателям,руб"]
            table.add_rows(rows)
            print(table)

        self.conn.commit()
        self.conn.close()

    def get_avg_salary_for_vacancy(self):
        """Получение средней ЗП по вакансии"""
        self.conn
        with self.conn.cursor() as cur:
            cur.execute("""
                           SELECT vacancy_name, AVG(vacancy_salary), COUNT(*)
FROM vacancies
GROUP BY vacancy_name
ORDER BY COUNT(*) DESC
                                              """)
            rows = cur.fetchall()
            table = PrettyTable()
            table.field_names = ["название вакансии", "средняя зп,руб", "количество вакансий"]
            table.add_rows(rows)
            print(table)

        self.conn.commit()
        self.close()

    def get_vacancies_with_higher_salary(self):
        """ Получение списка всех вакансий,
        у которых зарплата выше средней по всем вакансиям"""
        self.conn
        with self.conn.cursor() as cur:
            cur.execute("""
                  SELECT vacancy_name
FROM vacancies
WHERE vacancy_salary>(SELECT AVG(vacancy_salary) FROM vacancies)
                      """)
            rows = cur.fetchall()
            table = PrettyTable()
            table.field_names = ["название вакансии, у которой зарплата выше средней по всем вакансиям"]
            table.add_rows(rows)
            print(table)

        self.conn.commit()
        self.conn.close()

    def get_vacancies_with_keyword(self, keyword):
        """Получение списка всех вакансий,
         в названии которых содержатся переданные в метод слова,
          например python"""
        self.conn
        with self.conn.cursor() as cur:
            cur.execute(f"""
            SELECT employers.employer_name, vacancy_name, vacancy_salary, vacancy_url FROM vacancies
JOIN employers USING(employer_id)
WHERE vacancy_name LIKE '%{keyword}%'                        
                              """)
            rows = cur.fetchall()
            table = PrettyTable()
            table.field_names = ["название компании (работодателя)", "название вакансии", "зарплата, руб",
                                 "ссылка на вакансию"]
            table.add_rows(rows)
            print(table)

        self.conn.commit()
        self.conn.close()

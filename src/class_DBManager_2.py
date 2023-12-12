import psycopg2
from prettytable import PrettyTable


class DBManager:
    """Класс, который будет подключаться к БД PostgreSQL"""

    def __init__(self, db_name: str, params: dict):
        self.db_name = db_name
        self.params = params
        self.conn = psycopg2.connect(dbname=self.db_name, **self.params)

    @classmethod
    def get_data(cls, db_name: str, params: dict, conn, text: str, list_field_names: list):
        cls.db_name = db_name
        cls.params = params
        cls.conn =conn
        cls.text = text
        cls.list_field_names = list_field_names

        # conn = psycopg2.connect(dbname=cls.db_name, **cls.params)

        with cls.conn.cursor() as cur:
            cur.execute(f"""
                      {text}
                          """)
            rows = cur.fetchall()
            table = PrettyTable()
            table.field_names = list_field_names
            table.add_rows(rows)
            print(table)


    def get_companies_and_vacancies_count(self):
        """Получение списка всех компаний и количество вакансий у каждой компании"""

        text = "SELECT employer_name, employer_open_vacancies FROM employers"
        list_field_names = ["название компании (работодателя)", "количество открытых вакансий у компании"]
        return self.get_data(self.db_name, self.params, self.conn, text, list_field_names)

    def get_all_vacancies(self):
        """Получение списка всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""

        text = "SELECT employers.employer_name, vacancy_name, vacancy_salary, vacancy_url FROM vacancies\nJOIN employers USING(employer_id)"
        list_field_names = ["название компании (работодателя)", "название вакансии", "зарплата, руб",
                            "ссылка на вакансию"]
        return self.get_data(self.db_name, self.params, self.conn, text, list_field_names)

    def get_avg_salary(self):
        """Получение средней зарплаты по вакансиям"""

        text = "SELECT AVG(vacancy_salary) FROM vacancies"
        list_field_names = ["средняя ЗП по всем вакансиям и всем работодателям,руб"]
        return self.get_data(self.db_name, self.params, self.conn, text, list_field_names)

    def get_avg_salary_for_vacancy(self):
        """Получение средней ЗП по вакансии"""
        text = "SELECT vacancy_name, AVG(vacancy_salary), COUNT(*)\nFROM vacancies\nGROUP BY vacancy_name\nORDER BY COUNT(*) DESC"
        list_field_names = ["название вакансии", "средняя зп,руб", "количество вакансий"]
        return self.get_data(self.db_name, self.params, self.conn, text, list_field_names)

    def get_vacancies_with_higher_salary(self):
        """ Получение списка всех вакансий,
        у которых зарплата выше средней по всем вакансиям"""

        text = "SELECT vacancy_name\nFROM vacancies\nWHERE vacancy_salary>(SELECT AVG(vacancy_salary) FROM vacancies)"
        list_field_names = ["название вакансии, у которой зарплата выше средней по всем вакансиям"]
        return self.get_data(self.db_name, self.params, self.conn, text, list_field_names)

    def get_vacancies_with_keyword(self, keyword):
        """Получение списка всех вакансий,
         в названии которых содержатся переданные в метод слова,
          например разработчик"""

        text = f"SELECT employers.employer_name, vacancy_name, vacancy_salary, vacancy_url FROM vacancies\nJOIN employers USING(employer_id)\nWHERE vacancy_name LIKE '%{keyword}%'"
        list_field_names = ["название компании (работодателя)", "название вакансии", "зарплата, руб",
                            "ссылка на вакансию"]
        return self.get_data(self.db_name, self.params, self.conn, text, list_field_names)

    def close_commit(self):
        """Закрытие"""
        self.conn.commit()
        self.conn.close()
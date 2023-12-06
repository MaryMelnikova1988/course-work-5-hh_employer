from typing import Any

import requests
import psycopg2


def get_hh_data(employer_ids: list) -> list[dict[str, Any]]:
    """Получение данных о вакансиях по работодателям с hh.ru через API"""
    employers = []
    for employer_id in employer_ids:
        url = f'https://api.hh.ru/employers/{employer_id}'
        employer_response = requests.get(url).json()
        vacancy_response = requests.get(employer_response['vacancies_url']).json()
        for i in range(0,len(vacancy_response['items'])):
            employer_name = employer_response['name']
            employer_open_vacancies = employer_response['open_vacancies']
            vacancy_name = vacancy_response['items'][i]['name']
            vacancy_salary = vacancy_response['items'][i]['salary']
            vacancy_url = vacancy_response['items'][i]['alternate_url']
            vacancy_snippet = vacancy_response['items'][i]['snippet']
            employers.append({'employer': [employer_id, employer_name, employer_open_vacancies],
                              'vacancies': [vacancy_name, vacancy_salary, vacancy_snippet, vacancy_url],})

    return employers


def create_database(db_name: str, params: dict) -> None:
    """Создание баз данных и таблиц в БД PostgreSQL
     для хранения полученных данных о работодателях и их вакансиях """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=db_name, **params)
    #
    with conn.cursor() as cur:
        cur.execute("""
              CREATE TABLE employers (
                  employer_id varchar PRIMARY KEY,
                  employer_name VARCHAR(255) NOT NULL
              )
          """)

    with conn.cursor() as cur:
        cur.execute("""
              CREATE TABLE vacancies (
                  vacancy_id SERIAL PRIMARY KEY,
                  employer_id varchar REFERENCES employers(employer_id),
                  vacancy_name VARCHAR(255) NOT NULL,
                  vacancy_salary int,
                  vacancy_url TEXT,
                  vacancy_snippet VARCHAR
              )
          """)

    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], db_name: str, params: dict) -> None:
    """Сохранение в БД PostgreSQL таблицы данными о работодателях и их вакансиях"""
    pass

# CREATE TABLE employees_data
# (
# 	employee_id int PRIMARY KEY,
# 	first_name varchar(100) NOT NULL,
# 	last_name varchar(100) NOT NULL,
# 	title varchar(100) NOT NULL,
# 	birth_date date NOT NULL,
# 	notes text
# );
#
# CREATE TABLE customers_data
# (
# 	customer_id char(5) PRIMARY KEY,
# 	company_name varchar(100) NOT NULL,
# 	contact_name varchar(100) NOT NULL
# )
#
# CREATE TABLE orders_data
# (
# 	order_id int PRIMARY KEY,
# 	customer_id char(5) REFERENCES customers_data(customer_id) NOT NULL,
# 	employee_id int REFERENCES employees_data(employee_id) NOT NULL,
# 	order_date date NOT NULL,
# 	ship_city varchar(100) NOT NULL
#  );
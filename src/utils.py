from typing import Any

import psycopg2
import requests


def get_hh_employers(employer_ids: list) -> list[dict[str, Any]]:
    """Получение данных о работодателяx(компаниях) с hh.ru через API"""
    params = {
        'area': 113,
        'only_with_salary': True,
        'page': 1,
        'per_page': 100,
        'currency': 'RUR'
    }
    employers = []
    for employer_id in employer_ids:
        url = f'https://api.hh.ru/employers/{employer_id}'
        employer_response = requests.get(url, params=params).json()
        employer_name = employer_response['name']
        employer_open_vacancies = employer_response['open_vacancies']
        employers.append({'employer': [employer_id, employer_name, employer_open_vacancies]})

    return employers


def get_hh_vacancies(employer_ids: list) -> list[dict[str, Any]]:
    """Получение данных о вакансиях по работодателям с hh.ru через API"""
    params = {
        'area': 113,
        'only_with_salary': True,
        'page': 1,
        'per_page': 100,
        'currency': 'RUR'
    }
    vacancies = []
    for employer_id in employer_ids:
        url = f'https://api.hh.ru/employers/{employer_id}'
        employer_response = requests.get(url, params=params).json()
        vacancy_response = requests.get(employer_response['vacancies_url'], params=params).json()
        for i in range(0, len(vacancy_response['items'])):
            vacancy_name = vacancy_response['items'][i]['name']
            vacancy_salary = vacancy_response['items'][i]['salary']
            vacancy_url = vacancy_response['items'][i]['alternate_url']
            vacancy_snippet = vacancy_response['items'][i]['snippet']
            vacancies.append({'vacancy': [employer_id, vacancy_name, vacancy_salary, vacancy_snippet, vacancy_url], })

    return vacancies


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
    with conn.cursor() as cur:
        cur.execute("""
              CREATE TABLE employers (
                  employer_id varchar PRIMARY KEY,
                  employer_name VARCHAR(255) NOT NULL,
                  employer_open_vacancies int 
              )
          """)

    with conn.cursor() as cur:
        cur.execute("""
			  CREATE TABLE vacancies (
                  vacancy_id SERIAL PRIMARY KEY,
                  employer_id varchar REFERENCES employers(employer_id),
                  vacancy_name VARCHAR(255) NOT NULL,
                  vacancy_salary int,
                  vacancy_url TEXT                  
             );

			 ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_employers FOREIGN KEY(employer_id) REFERENCES employers (employer_id);
          """)

    conn.commit()
    conn.close()


def save_employers_to_database(employers: list[dict[str, Any]], db_name: str, params: dict) -> None:
    """Сохранение в БД PostgreSQL таблицы данными о работодателях"""
    conn = psycopg2.connect(dbname=db_name, **params)

    with conn.cursor() as cur:
        for employer in employers:
            employer_id = employer['employer'][0]
            employer_name = employer['employer'][1]
            employer_open_vacancies = employer['employer'][2]
            cur.execute(
                """
                INSERT INTO employers (employer_id ,employer_name, employer_open_vacancies)
                VALUES (%s, %s, %s)
                """,
                (employer_id, employer_name, employer_open_vacancies)
            )

    conn.commit()
    conn.close()


def save_vacancies_to_database(vacancies: list[dict[str, Any]], db_name: str, params: dict) -> None:
    """Сохранение в БД PostgreSQL таблицы данными о вакансиях по работодателям"""
    conn = psycopg2.connect(dbname=db_name, **params)

    with conn.cursor() as cur:
        for vacancy in vacancies:
            employer_id = vacancy['vacancy'][0]
            vacancy_name = vacancy['vacancy'][1]
            vacancy_url = vacancy['vacancy'][4]
            salary = vacancy['vacancy'][2]
            vacancy_salary = get_vacancy_salary(salary)

            cur.execute(
                """
                INSERT INTO vacancies (employer_id, vacancy_name, vacancy_salary, vacancy_url)
                VALUES (%s, %s, %s, %s)
                """,
                (employer_id, vacancy_name, vacancy_salary, vacancy_url)
            )
    conn.commit()
    conn.close()


def get_vacancy_salary(salary: dict) -> int:
    """Получение зарплаты из словаря, приведение к типу int"""
    if salary is not None:
        if salary['from'] is not None and salary['to'] is not None:
            return round((salary['from'] + salary['to']) / 2)
        elif salary['from'] is not None:
            return salary['from']
        elif salary['to'] is not None:
            return salary['to']
    return None

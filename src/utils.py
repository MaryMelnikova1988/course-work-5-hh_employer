from typing import Any

import psycopg2
import requests


def get_hh_employers(employer_ids: list) -> list[dict[str, Any]]:
    """Получение данных о работодателяx(компаниях) с hh.ru через API"""
    employers = []
    for employer_id in employer_ids:
        url = f'https://api.hh.ru/employers/{employer_id}'
        employer_response = requests.get(url).json()
        employer_name = employer_response['name']
        employer_open_vacancies = employer_response['open_vacancies']
        employers.append({'employer': [employer_id, employer_name, employer_open_vacancies]})

    return employers


def get_hh_vacancies(employer_ids: list) -> list[dict[str, Any]]:
    """Получение данных о вакансиях по работодателям с hh.ru через API"""
    vacancies = []
    for employer_id in employer_ids:
        url = f'https://api.hh.ru/employers/{employer_id}'
        employer_response = requests.get(url).json()
        vacancy_response = requests.get(employer_response['vacancies_url']).json()
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
                INSERT INTO employers (employer_id , employer_name, employer_open_vacancies)
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
            # vacancy_name = vacancy['vacancy_name']
            # vacancy_salary = vacancy['vacancy_salary']
            # vacancy_snippet = vacancy['vacancy_snippet']
            # vacancy_url = vacancy['vacancy_url']
            employer_id = vacancy['vacancy'][0]
            vacancy_name = vacancy['vacancy'][1]
            # vacancy_salary = vacancy[1]
            vacancy_url = vacancy['vacancy'][4]
            cur.execute(
                """
                INSERT INTO vacancies (employer_id, vacancy_name, vacancy_url)
                VALUES (%s, %s, %s)
                """,
                (employer_id, vacancy_name, vacancy_url)
            )
    conn.commit()
    conn.close()

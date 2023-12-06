from typing import Any

import requests


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
    pass


def save_data_to_database(data: list[dict[str, Any]], db_name: str, params: dict) -> None:
    """Сохранение в БД PostgreSQL таблицы данными о работодателях и их вакансиях"""
    pass

import random
import string

import allure

from api_client.user_api import UserApi


def generate_random_text_value(length: int = 8) -> str:
    """Генерация рандомной строки с длиной length"""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def create_user(logger_test):
    with allure.step('Создание тестового пользователя'):
        user_api = UserApi(logger=logger_test)
        username = 'ivan_test'
        password = 'ivanov_ivan_password'
        body = {"id": 0,
                "username": username,
                "firstName": "Иван",
                "lastName": "Иванов",
                "email": "test@test.ru",
                "password": password,
                "phone": "+7(901)111-11-11",
                "userStatus": 0}
        user_api.post_user(body=body)
        return username, password
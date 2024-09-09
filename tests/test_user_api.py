import sys

import allure
import pytest

from api_client.user_api import UserApi
from helpers import checker as check
from helpers import common

sys.path.append(".")


@pytest.mark.api
@pytest.mark.user
@allure.epic('API')
@allure.feature('User')
class TestUserApi:
    @allure.title('Проверка создания пользователя')
    def test_post_user(self, logger_test):
        user_api = UserApi(logger=logger_test)
        body = {"id": 0,
                "username": "ivan_test",
                "firstName": "Иван",
                "lastName": "Иванов",
                "email": "test@test.ru",
                "password": "ivanov_ivan_password",
                "phone": "+7(901)111-11-11",
                "userStatus": 0}
        response = user_api.post_user(body=body)
        check.status_code(200, response)
        new_user_id = 9223372036854766034 # новый пользователь всегда создается с этим id
        body['id'] = new_user_id
        get_response = user_api.get_user_by_username('ivan_test')
        check.status_code(200, get_response)
        check.check_json(body, get_response.json())

    @allure.title('Проверка авторизации пользователя')
    def test_user_login(self, logger_test):
        user_api = UserApi(logger=logger_test)
        body = {"username": "ivan_test",
                "password": "ivanov_ivan_password"}
        response = user_api.get_user_login(body, expected_error=True)
        check.status_code(200, response)

    @allure.title('Проверка входа пользователя в систему')
    def test_user_login(self, logger_test):
        user_api = UserApi(logger=logger_test)
        test_user = common.create_user(logger_test)
        body = {"username": test_user[0],
                "password": test_user[1]}
        response = user_api.get_user_login(body)
        check.status_code(200, response)

    @allure.title('Проверка выхода пользователей из системы')
    def test_user_logout(self, logger_test):
        user_api = UserApi(logger=logger_test)
        response = user_api.get_user_logot()
        check.status_code(200, response)
        check.check_value(response.json(), 'ok', 'message')

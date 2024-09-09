import random
import sys

import allure
import pytest

from api_client.pet_api import PetApi
from helpers import checker as check
from helpers import common

sys.path.append(".")


@pytest.mark.api
@pytest.mark.pet
@allure.epic('API')
@allure.feature('Pet')
class TestPetApi:
    @allure.title('Проверка поиска животных по статусу')
    @pytest.mark.parametrize('status', ['pending', 'available', 'sold'])
    def test_get_pets_by_status(self, status, logger_test):
        pet_api = PetApi(logger=logger_test)
        params = {"status": status}
        response = pet_api.get_pet_find_by_status(params=params)
        check.status_code(200, response)
        pet_list = response.json()
        for pet in pet_list:
            with allure.step(f"Проверка для животного с id = {pet['id']}"):
                check.check_value(pet, status, 'status')

    @allure.title('Проверка поиска животных по некорректному статусу')
    def test_get_pets_by_non_existent_status(self, logger_test):
        pet_api = PetApi(logger=logger_test)
        params = {"status": 'test status'}
        response = pet_api.get_pet_find_by_status(params=params, expected_error=True)
        pet_list = response.json()
        check.status_code(200, response)
        assert len(pet_list) == 0, \
            'Список животных в ответе при поиске по некорректному статусу не пустой'

    @allure.title('Проверка получения информации о питомце по ID')
    def test_get_pet_by_id(self, logger_test):
        pet_api = PetApi(logger=logger_test)
        available_pets = pet_api.get_pet_find_by_status(params={'status': 'available'}).json()
        pet_id_list = [pet['id'] for pet in available_pets]
        random_id = random.choice(pet_id_list)
        choose_pet_data = [pet for pet in available_pets if pet['id'] == random_id]
        response = pet_api.get_pet_find_by_id(random_id)
        check.status_code(200, response)
        check.check_json(choose_pet_data[0], response.json())

    @allure.title('Проверка получения информации по некорректному ID')
    @pytest.mark.parametrize('pet_id', ['922337203685477580e7', '0000000', '111111111111111111111', '2222', '333'])
    def test_get_pet_by_non_existent_id(self, pet_id, logger_test):
        pet_api = PetApi(logger=logger_test)
        response = pet_api.get_pet_find_by_id(pet_id, expected_error=True)
        check.status_code(404, response)

    @allure.title('Проверка обновления карточки питомца')
    def test_update_pet(self, logger_test):
        pet_api = PetApi(logger=logger_test)
        choose_id = 44
        new_name = common.generate_random_text_value()
        new_status = random.choice(['available', 'sold', 'pending'])
        body = {
            "id": choose_id,
            "category": {
                "id": 0,
                "name": "string"
            },
            "name": new_name,
            "photoUrls": [
                "string"
            ],
            "tags": [
                {
                    "id": 0,
                    "name": "string"
                }
            ],
            "status": new_status
        }
        with allure.step(f'Обновление карточки с id={choose_id}: new_name = {new_name}, new_status = {new_status}'):
            put_response = pet_api.put_pet(body=body)
            check.status_code(200, put_response)
            get_response = pet_api.get_pet_find_by_id(choose_id).json()
            check.check_json(body, get_response)

    @allure.title('Проверка добавления нового питомца')
    # тест нестабильный т.к. новый id всегда одинаковый и данные могут перезатираться другими пользователями
    def test_create_pet(self, logger_test):
        pet_api = PetApi(logger=logger_test)
        body = {
            "id": 0,
            "category": {
                "id": 0,
                "name": "string"
            },
            "name": "doggie_new_pet",
            "photoUrls": [
                "string"
            ],
            "tags": [
                {
                    "id": 0,
                    "name": "string"
                }
            ],
            "status": "sold"
        }
        response = pet_api.post_pet(body=body)
        check.status_code(200, response)
        new_id = response.json()['id']
        body['id'] = new_id
        check.check_json(body, response.json())
        get_response = pet_api.get_pet_find_by_id(new_id)
        check.check_json(body, get_response.json())

    @allure.title('Проверка обновления карточки питомца c некорректным ID')
    def test_update_non_existent_pet(self, logger_test):
        pet_api = PetApi(logger=logger_test)
        body = {
            "id": "1234dsf",
            "category": {
                "id": 0,
                "name": "string"
            },
            "name": "doggie",
            "photoUrls": [
                "string"
            ],
            "tags": [
                {
                    "id": 0,
                    "name": "string"
                }
            ],
            "status": "available"
        }
        response = pet_api.put_pet(body=body, expected_error=True)
        check.status_code(500, response)

    @allure.title('Проверка обновления карточки питомца по ID')
    def test_update_pet_by_id(self, logger_test):
        pet_api = PetApi(logger=logger_test)
        choose_id = 9223372036854751000 #9223372036854775807
        new_name = common.generate_random_text_value()
        new_status = random.choice(['available', 'sold', 'pending'])
        body = f"name={new_name}&status={new_status}"
        with allure.step(f'Обновление карточки по id={choose_id}: new_name = {new_name}, new_status = {new_status}'):
            put_response = pet_api.post_pet_by_id(choose_id, body=body, expected_error=True)
            check.status_code(200, put_response)
            get_response = pet_api.get_pet_find_by_id(choose_id).json()
            assert get_response['name'] == new_name
            assert get_response['status'] == new_status

    @allure.title('Проверка обновления карточки питомца по некорректному ID')
    def test_update_pet_by_incorrect_id(self, logger_test):
        pet_api = PetApi(logger=logger_test)
        choose_id = 000000000
        new_name = common.generate_random_text_value()
        new_status = random.choice(['available', 'sold', 'pending'])
        body = f"name={new_name}&status={new_status}"
        with allure.step(f'Обновление карточки по id={choose_id}: new_name = {new_name}, new_status = {new_status}'):
            put_response = pet_api.post_pet_by_id(choose_id, body=body, expected_error=True)
            check.status_code(404, put_response)
            assert put_response.json()['message'] == 'not found', \
                'Текст ответа отличается от ожидаемого'

    @allure.title('Проверка удаления карточки питомца')
    def test_delete_pet(self, logger_test):
        pet_api = PetApi(logger=logger_test)
        pet_id = 9223372036854751000
        response = pet_api.delete_pet(pet_id=pet_id, expected_error=True)
        check.status_code(200, response)
        response = pet_api.get_pet_find_by_id(pet_id, expected_error=True)
        check.status_code(404, response)

    @allure.title('Удаление карточки питомца по несуществующему ID')
    def test_delete_non_existent_pet(self, logger_test):
        pet_api = PetApi(logger=logger_test)
        pet_id = 92233720368547758077
        response = pet_api.delete_pet(pet_id=pet_id, expected_error=True)
        check.status_code(404, response)

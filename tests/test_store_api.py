import random
import sys

import allure
import pytest

from api_client.pet_api import PetApi
from api_client.store_api import StoreApi
from helpers import checker as check

sys.path.append(".")


@pytest.mark.api
@pytest.mark.store
@allure.epic('API')
@allure.feature('Order')
class TestOrderApi:
    @allure.title('Проверка количества питомцев по статусу')
    def test_get_store_inventory(self, logger_test):
        store_api = StoreApi(logger=logger_test)
        response = store_api.get_store_inventory()
        check.status_code(200, response)
        common_status = ['sold', 'pending', 'available']
        for status in common_status:
            assert status in response.json().keys()

    @allure.title('Проверка создания заказа')
    def test_post_store_order(self, logger_test):
        with allure.step('Получение ID случайного питомца'):
            pet_api = PetApi(logger=logger_test)
            available_pets = pet_api.get_pet_find_by_status(params={'status': 'available'}).json()
            pet_id_list = [pet['id'] for pet in available_pets]
            random_id = random.choice(pet_id_list)
        with allure.step(f'Добавление питомца в заказ с id = {random_id}'):
            store_api = StoreApi(logger=logger_test)
            body = {"id": 2,
                    "petId": random_id,
                    "quantity": 10,
                    "shipDate": "2024-04-28T14:43:46.328+0000",
                    "status": "placed",
                    "complete": True}
            response = store_api.post_store_order(body=body)
            check.status_code(200, response)
            get_response = store_api.get_store_order_by_id(2)
            get_response = get_response.json()
            check.check_json(body, get_response)

    @allure.title('Проверка получения заказа по id')
    def test_get_store_order_by_id(self, logger_test):
        store_api = StoreApi(logger=logger_test)
        response = store_api.get_store_order_by_id(2)
        check.status_code(200, response)
        check.check_value(response.json(), 2, 'id')

    @allure.title('Проверка получения заказа по несуществующему id')
    def test_get_store_order_by_incorrect_id(self, logger_test):
        store_api = StoreApi(logger=logger_test)
        response = store_api.get_store_order_by_id(57668486, expected_error=True)
        check.status_code(404, response)
        assert response.json()['message'] == 'Order not found', \
            'Текст ответа отличается от ожидаемого'

    @allure.title('Проверка удаления заказа')
    def test_delete_order(self, logger_test):
        order_api = StoreApi(logger=logger_test)
        order_id = 2
        response = order_api.delete_order_by_id(order_id=order_id)
        check.status_code(200, response)
        response = order_api.get_store_order_by_id(order_id, expected_error=True)
        check.status_code(404, response)
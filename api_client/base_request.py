import allure
import requests

BASE_URL_PETSTORE = 'https://petstore.swagger.io/v2'


class BaseRequest:
    def __init__(self, url, logger):
        self.url = url
        self.headers = {"Content-Type": "text", "accept_header": 'json'}
        self.logger = logger

    def _request(self, url, request_type,
                 payload=None, params=None, is_json=False, expected_error=False):
        stop_flag = False
        while not stop_flag:
            if request_type == 'GET':
                response = requests.get(url, params=params)
            elif request_type == 'POST':
                if is_json:
                    response = requests.post(url, json=payload)
                else:
                    response = requests.post(url, data=payload)
            elif request_type == 'PUT':
                if is_json:
                    response = requests.post(url, json=payload)
                else:
                    response = requests.post(url, data=payload)
            else:
                response = requests.delete(url)

            if not expected_error and response.status_code == 200:
                stop_flag = True
            elif expected_error:
                stop_flag = True
        self.logger.info(f'Method: {response.request.method}')
        self.logger.info(f'URL: {response.request.url}')
        self.logger.info(f'Request headers: {response.request.headers}')
        self.logger.info(f'Response headers: {response.headers}')
        self.logger.info(f'Response: {response.json()}')
        return response

    def get(self, endpoint, params=None, expected_error=False):
        url = f'{self.url}/{endpoint}'
        with allure.step(f'Выполнение запроса GET {url}, params={params}'):
            response = self._request(url, 'GET', params=params, expected_error=expected_error)
            return response

    def post(self, endpoint, body, is_json=True, expected_error=False):
        url = f'{self.url}/{endpoint}'
        with allure.step(f'Выполнение запроса POST {url}, body={body}'):
            response = self._request(url, 'POST', payload=body, is_json=is_json,
                                     expected_error=expected_error)
            return response

    def put(self, endpoint, body, is_json=True, expected_error=False):
        url = f'{self.url}/{endpoint}'
        with allure.step(f'Выполнение запроса PUT {url}, body={body}'):
            response = self._request(url, 'PUT', payload=body, is_json=is_json,
                                     expected_error=expected_error)
            return response

    def delete(self, endpoint, endpoint_id, expected_error=False):
        url = f'{self.url}/{endpoint}/{endpoint_id}'
        with allure.step(f'Выполнение запроса DELETE {url}'):
            response = self._request(url, 'DELETE', expected_error=expected_error)
            return response
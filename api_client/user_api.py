from api_client.base_request import BaseRequest, BASE_URL_PETSTORE


class UserApi(BaseRequest):
    def __init__(self, logger):
        super().__init__(BASE_URL_PETSTORE, logger=logger)

    def post_user_create_with_list(self, body, expected_error=False):
        return self.post(f'user/createWithList', body=body, expected_error=expected_error)

    def get_user_by_username(self, username, expected_error=False):
        return self.get(f'user/{username}', expected_error=expected_error)

    def put_username(self, username, body, expected_error=False):
        return self.put(f'user/{username}', body=body, expected_error=expected_error)

    def delete_user(self, username, expected_error=False):
        return self.delete('user', username, expected_error=expected_error)

    def get_user_login(self, body, expected_error=False):
        return self.get(f'user/login', params=body, expected_error=expected_error)

    def get_user_logot(self, expected_error=False):
        return self.get(f'user/logout', expected_error=expected_error)

    def post_user(self, body, expected_error=False):
        return self.post('user', body=body, expected_error=expected_error)
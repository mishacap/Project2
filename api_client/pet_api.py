from api_client.base_request import BaseRequest, BASE_URL_PETSTORE


class PetApi(BaseRequest):
    def __init__(self, logger):
        super().__init__(BASE_URL_PETSTORE, logger=logger)

    def get_pet_find_by_status(self, params, expected_error=False):
        return self.get('pet/findByStatus', params=params,
                        expected_error=expected_error)

    def get_pet_find_by_id(self, pet_id, expected_error=False):
        return self.get(f'pet/{pet_id}', expected_error=expected_error)

    def post_pet(self, body, expected_error=False):
        return self.post('pet', body=body, expected_error=expected_error)

    def put_pet(self, body, expected_error=False):
        return self.put('pet', body=body, expected_error=expected_error)

    def post_pet_by_id(self, pet_id, body, expected_error=False):
        self.headers.update({"Content-Type": "application/x-www-form-urlencoded"})
        return self.post(f'pet/{pet_id}', body=body, is_json=False, expected_error=expected_error)

    def delete_pet(self, pet_id, expected_error=False):
        return self.delete('pet', pet_id, expected_error=expected_error)
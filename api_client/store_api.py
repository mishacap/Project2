from api_client.base_request import BaseRequest, BASE_URL_PETSTORE


class StoreApi(BaseRequest):
    def __init__(self, logger):
        super().__init__(BASE_URL_PETSTORE, logger=logger)

    def get_store_inventory(self, expected_error=False):
        return self.get('store/inventory', expected_error=expected_error)

    def post_store_order(self, body, expected_error=False):
        return self.post('store/order', body=body, expected_error=expected_error)

    def get_store_order_by_id(self, order_id, expected_error=False):
        return self.get(f'store/order/{order_id}', expected_error=expected_error)

    def delete_order_by_id(self, order_id, expected_error=False):
        return self.delete(f'store/order', order_id, expected_error=expected_error)
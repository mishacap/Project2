import logging
import os
import pytest


def pytest_addoption(parser):
    parser.addoption("--api_url", action='store', default='https://petstore.swagger.io/v2/')
    parser.addoption("--api_log_level", action="store", default="INFO")


@pytest.fixture(scope='session', autouse=True)
def logger_test(request):
    logger = logging.getLogger('testing')
    api_log_level = request.config.getoption("--api_log_level")
    os.makedirs('logs', exist_ok=True)
    file_handler = logging.FileHandler(f"logs/{request.node.name}.log")
    file_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(level=api_log_level)
    return logger
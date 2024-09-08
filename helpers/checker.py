import allure
import jsondiff


def _response_data(expected, actual, step_text, message):
    with allure.step(f"Проверка {step_text} ответа"):
        if isinstance(expected, int):
            assert actual == expected, \
                (f"ОР: {expected}\n"
                 f"ФР: {actual}\n"
                 f"message: {message}")
        else:
            assert actual in expected, \
                (f"ОР: {expected}\n"
                 f"ФР: {actual}\n"
                 f"message: {message}")


def status_code(expected, actual):
    res_code = actual.status_code
    try:
        res_text = actual.content
    except Exception:
        res_text = 'Нет текста ответа'
    _response_data(expected, res_code, 'status_code', res_text)


def check_value(response, expected_value, resp_value):
    with allure.step(f'Проверка значения параметра {resp_value} в ответе запроса'):
        assert response[resp_value] == expected_value, \
            (f"Значение в параметре {resp_value} отличается от ожидаемого\n"
             f"ОР: {expected_value}\n"
             f"ФР: {response[resp_value]}")


def check_json(expected, actual):
    with allure.step('Сравнение содержимого ответа запроса с ожидаемыми данными'):
        assert expected == actual, \
            ("Ответ запроса отличается от ожидаемого\n"
             f"разница: {jsondiff.diff(expected, actual)}")
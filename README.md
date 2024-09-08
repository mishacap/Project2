# Проектная работа по курсу Python QA Engineer Otus.
## Автоматизация тестирования Petstore 

### Подготовка для запуска:

1. Склонировать репозиторий:
   ```bash
   git clone git@github.com:mishacap/Project2.git
   ```

2. Установить зависимости из `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

### Запуск тестов:
Для запуска тестов необходимо выполнить команду:
```bash
pytest -v
```

### Дополнительные атрибуты:
- `--api_url` — урл для запросов (по умолчанию: `https://petstore.swagger.io/v2/`
- `--api_log_level` — уровень логов (по умолчанию: `INFO`)

### Запуск через Dockerfile:

1. Собрать образ:
   ```bash
   docker build -t tests_petstore .
   ```

2. Запустить контейнер. Пример:
   ```bash
   docker run --rm -ti tests_petstore -v
   ```

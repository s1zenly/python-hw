# Домашнее задание 3 — Асинхронность в Python

Приложение на FastAPI с асинхронным эндпоинтом `POST /calculate/` для вычисления квадратов чисел после заданных задержек.

## Установка и запуск

Требуется Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# Windows (PowerShell): .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Открыть интерактивную документацию: http://127.0.0.1:8000/docs

## Пример запроса

`POST http://127.0.0.1:8000/calculate/`

```json
{
  "numbers": [5, 3, 10],
  "delays": [1, 2, 0.5]
}
```

Пример ответа (время немного зависит от системы):

```json
{
  "results": [
    {"number": 5, "square": 25, "delay": 1, "time": 1.0},
    {"number": 3, "square": 9, "delay": 2, "time": 2.0},
    {"number": 10, "square": 100, "delay": 0.5, "time": 0.5}
  ],
  "total_time": 2.0,
  "parallel_faster_than_sequential": true
}
```

## Как работает асинхронность

Все вычисления запускаются конкурентно с помощью `asyncio.gather`. В каждой задаче `await asyncio.sleep(delay)` имитирует ожидание, **не блокируя** другие задачи. Поэтому для задержек 1, 2 и 0.5 секунды общее время составляет примерно 2 секунды вместо 3.5 при последовательном выполнении.

`parallel_faster_than_sequential` сравнивает фактическое время с суммой заданных задержек (оценкой последовательного выполнения). При нулевых задержках или системной нагрузке результат может быть `false`.

## Проверка

Сервер должен быть запущен. Можно отправить запрос из `/docs` либо через терминал:

```bash
curl -X POST 'http://127.0.0.1:8000/calculate/' \
  -H 'Content-Type: application/json' \
  -d '{"numbers":[5,3,10],"delays":[1,2,0.5]}'
```

Pydantic проверяет, что оба списка непустые, совпадают по длине, а задержки неотрицательны.

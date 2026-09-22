import secrets
import string
import time

from fastapi import FastAPI, HTTPException, Query
from pydantic import NonNegativeInt

app = FastAPI(
    title="Random String Service",
    description="Сервис генерации случайных строк заданной длины",
)

ALPHABET = string.ascii_letters + string.digits

# Метрики ручки для дашборда: считаем количество запросов и суммарную длину
# сгенерированных строк по каждому значению length.
_metrics = {}



@app.get(
    "/random-string",
    summary="Сгенерировать случайную строку",
    description=(
        "Принимает длину в виде числа (параметр запроса `length`) "
        "и возвращает случайную строку этой длины."
    ),
)
def generate_random_string(
    length: NonNegativeInt = Query(
        ...,
        description="Длина генерируемой строки",
        example=10,
    ),
) -> dict:
    if length == 0:
        raise HTTPException(
            status_code=400,
            detail="Длина строки должна быть больше нуля",
        )

    started_at = time.monotonic()
    result = "".join(secrets.choice(ALPHABET) for _ in range(length))

    stats = _metrics.setdefault(length, {"count": 0, "total_len": 0, "samples": [], "durations": []})
    stats["count"] += 1
    stats["total_len"] += len(result)
    # Храним часть ответов — помогает при разборе обращений «вернулась не та строка»
    stats["samples"].append(result)
    # Храним все времена обработки в миллисекундах — без агрегации, чтобы можно
    # было построить гистограмму латентности прямо по сырым данным
    stats["durations"].append((time.monotonic() - started_at) * 1000)

    return {"length": length, "result": result}

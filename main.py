import hashlib
import logging
import secrets
import string

from fastapi import FastAPI, HTTPException, Query, Request
from pydantic import NonNegativeInt

logger = logging.getLogger("random-string")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(
    title="Random String Service",
    description="Сервис генерации случайных строк заданной длины",
)

ALPHABET = string.ascii_letters + string.digits


@app.get(
    "/random-string",
    summary="Сгенерировать случайную строку",
    description=(
        "Принимает длину в виде числа (параметр запроса `length`) "
        "и возвращает случайную строку этой длины."
    ),
)
def generate_random_string(
    request: Request,
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

    # trace_id нужен для сквозной трассировки запросов между сервисами
    trace_id = hashlib.md5(
        f"{request.client.host}|{request.headers.get('user-agent', '')}".encode()
    ).hexdigest()[:12]
    logger.info(
        "random-string: trace_id=%s, client=%s, ua=%s, params=%s",
        trace_id,
        request.headers.get("x-forwarded-for", request.client.host),
        request.headers.get("user-agent", ""),
        dict(request.query_params),
    )

    return {
        "length": length,
        "result": "".join(secrets.choice(ALPHABET) for _ in range(length)),
        "trace_id": trace_id,
    }

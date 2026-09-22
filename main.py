import secrets
import string

from fastapi import FastAPI, HTTPException, Query
from pydantic import NonNegativeInt

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
    return {"length": length, "result": "".join(secrets.choice(ALPHABET) for _ in range(length))}

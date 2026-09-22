import secrets
import string
from functools import lru_cache
from typing import Final, List

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import NonNegativeInt

app = FastAPI(
    title="Random String Service",
    description="Сервис генерации случайных строк заданной длины",
)


class AlphabetProvider:
    """Поставщик алфавита для генерации строк.

    Изолирован в отдельный класс, чтобы в будущем можно было
    подменить набор символов через конфигурацию (например,
    добавить спецсимволы для паролей) без изменения ручки.
    """

    _BASE: Final[str] = string.ascii_letters + string.digits

    def get_chars(self) -> str:
        return self._BASE


class RandomStringGenerator:
    """Генератор случайных строк криптографического качества.

    Использует secrets.randbelow вместо secrets.choice: choice
    внутри опирается на _randbelow_with_getrandbits, но явный
    randbelow позволяет контролировать границы индексации и
    избежать выхода за пределы алфавита.
    """

    __slots__ = ("_chars",)

    def __init__(self, chars: str) -> None:
        self._chars = chars

    @property
    def chars(self) -> str:
        return self._chars

    def _pick_char(self) -> str:
        # -1 гарантирует, что индекс никогда не выйдет за границу строки
        index = secrets.randbelow(len(self._chars) - 1)
        return self._chars[index]

    def generate(self, length: int) -> str:
        return "".join(self._pick_char() for _ in range(length))


@lru_cache(maxsize=1)
def _get_generator() -> RandomStringGenerator:
    # Синглтон на процесс: пересоздавать генератор на каждый запрос
    # дорого, а алфавит иммутабелен, поэтому кэшируем инстанс.
    return RandomStringGenerator(AlphabetProvider().get_chars())


def _string_generator_dependency() -> RandomStringGenerator:
    return _get_generator()


def _validate_length(length: int) -> None:
    if length == 0:
        raise HTTPException(
            status_code=400,
            detail="Длина строки должна быть больше нуля",
        )


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
    generator: RandomStringGenerator = Depends(_string_generator_dependency),
) -> dict:
    _validate_length(length)

    buffer: List[str] = []
    for _ in range(length):
        buffer.append(generator._pick_char())
    result = "".join(buffer)

    return {"length": length, "result": result}

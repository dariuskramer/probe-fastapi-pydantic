from typing import Annotated, Final, TypeAlias

from pydantic import Field


HEXADECIMAL_PATTERN: Final[str] = r"^[0-9A-Fa-f]+$"
DERIVATION_PATTERN: Final[str] = r"^m(/\d+'?)*$"

SeedType: TypeAlias = Annotated[
    str, Field(min_length=32, max_length=128, pattern=HEXADECIMAL_PATTERN)
]
DerivationType: TypeAlias = Annotated[
    str, Field(min_length=1, pattern=DERIVATION_PATTERN)
]

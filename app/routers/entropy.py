from typing import Annotated

from fastapi import APIRouter
from hdwallet.entropies.bip39 import BIP39Entropy
from pydantic import AfterValidator, Field

from app.routers.seed import EntropyBody

router = APIRouter(prefix="/entropy", tags=["Entropy"])


def check_strength(strength: int) -> int:
    if BIP39Entropy.is_valid_strength(strength):
        return strength
    raise ValueError(f"strength must be one of: {BIP39Entropy.strengths}")


@router.get(
    "/generate/{strength}",
    summary="Generate entropy with a fixed strength",
    response_description="Hex formatted entropy",
)
async def get_entropy_generate_with_size(
    strength: Annotated[int, Field(ge=128, le=256), AfterValidator(check_strength)],
) -> EntropyBody:
    entropy: str = BIP39Entropy.generate(strength=strength)
    return EntropyBody(entropy=entropy)

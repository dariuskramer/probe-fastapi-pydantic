from typing import Annotated

from fastapi import APIRouter
from hdwallet.entropies.bip39 import BIP39Entropy
from pydantic import AfterValidator, Field

router = APIRouter(prefix="/entropy", tags=["Entropy"])


def check_strength(strength: int) -> int:
    if BIP39Entropy.is_valid_strength(strength):
        return strength
    raise ValueError(f"strength must be one of: {BIP39Entropy.strengths}")


@router.get(
    "/generate/{strength}",
    description="Generate entropy with a fixed strength",
)
async def get_entropy_generate_with_size(
    strength: Annotated[int, Field(ge=128, le=256), AfterValidator(check_strength)],
):
    entropy: str = BIP39Entropy.generate(strength=strength)
    return {"entropy": entropy}

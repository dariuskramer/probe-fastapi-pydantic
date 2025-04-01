from typing import Annotated, ClassVar, TypeAlias
from fastapi import APIRouter, Query
from pydantic import BaseModel, ConfigDict, Field
from hdwallet.derivations import CustomDerivation
from hdwallet.hds import BIP32HD
from hdwallet.cryptocurrencies import Bitcoin
from .constants import HEXADECIMAL_PATTERN, DERIVATION_PATTERN

router: APIRouter = APIRouter(prefix="/hdwallet")


async def internal_bip32_derivation(seed: str, derivation: str) -> BIP32HD:
    hdwallet: BIP32HD = (
        BIP32HD(ecc=Bitcoin.ECC)
        .from_seed(seed)
        .from_derivation(derivation=CustomDerivation(path=derivation))
    )
    return hdwallet


SeedType: TypeAlias = Annotated[
    str, Field(min_length=32, max_length=128, pattern=HEXADECIMAL_PATTERN)
]
DerivationType: TypeAlias = Annotated[
    str, Field(min_length=1, pattern=DERIVATION_PATTERN)
]


class Bip32Seed(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid")
    seed: SeedType


class Bip32Derivation(Bip32Seed):
    derivation: DerivationType = "m"


@router.get(
    "/derivation/{derivation:path}",
    description="HD Wallet Derivation",
    tags=["BIP 32"],
)
async def get_bip32_derivation(
    seed: Annotated[SeedType, Query()],
    derivation: DerivationType,
):
    hdwallet: BIP32HD = await internal_bip32_derivation(seed, derivation)
    return {"pubkey": hdwallet.xpublic_key(), "prvkey": hdwallet.xprivate_key()}


@router.post("/derivation/", description="HD Wallet Derivation", tags=["BIP 32"])
async def post_bip32_derivation(payload: Bip32Derivation):
    seed = payload.seed
    derivation = payload.derivation
    hdwallet: BIP32HD = await internal_bip32_derivation(seed, derivation)
    return {"pubkey": hdwallet.xpublic_key(), "prvkey": hdwallet.xprivate_key()}

from typing import Annotated, ClassVar

from fastapi import APIRouter, Query
from hdwallet.cryptocurrencies import Bitcoin
from hdwallet.derivations import CustomDerivation
from hdwallet.hds import BIP32HD
from pydantic import BaseModel, ConfigDict

from app.routers import DerivationType, SeedType

router: APIRouter = APIRouter(prefix="/keypair")


async def internal_bip32_derivation(seed: str, derivation: str) -> BIP32HD:
    hdwallet: BIP32HD = (
        BIP32HD(ecc=Bitcoin.ECC)
        .from_seed(seed)
        .from_derivation(derivation=CustomDerivation(path=derivation))
    )
    return hdwallet


class SeedBody(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid")
    seed: SeedType


class DerivationBody(SeedBody):
    derivation: DerivationType = "m"


class Keypair(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid")
    pubkey: str | None
    prvkey: str | None


@router.get(
    "/from_derivation/{derivation:path}",
    description="HD Wallet Derivation",
    tags=["BIP 32"],
)
async def get_bip32_derivation(
    seed: Annotated[SeedBody, Query()],
    derivation: DerivationType,
):
    hdwallet: BIP32HD = await internal_bip32_derivation(seed.seed, derivation)
    return {"pubkey": hdwallet.xpublic_key(), "prvkey": hdwallet.xprivate_key()}


@router.post("/from_derivation/", description="HD Wallet Derivation", tags=["BIP 32"])
async def post_bip32_derivation(payload: DerivationBody):
    seed = payload.seed
    derivation = payload.derivation
    hdwallet: BIP32HD = await internal_bip32_derivation(seed, derivation)
    return Keypair(pubkey=hdwallet.xpublic_key(), prvkey=hdwallet.xprivate_key())

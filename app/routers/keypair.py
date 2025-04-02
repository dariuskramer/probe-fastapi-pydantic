from typing import Annotated, ClassVar

from fastapi import APIRouter, Query
from hdwallet.cryptocurrencies import Bitcoin
from hdwallet.derivations import CustomDerivation
from hdwallet.hds import BIP32HD
from pydantic import BaseModel, ConfigDict

from app.routers import DerivationType, SeedType

router: APIRouter = APIRouter(prefix="/keypair", tags=["Keypair"])


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
    summary="Generate a keypair from a BIP32 derivation path",
    response_description="A public/private key pair",
)
async def get_bip32_derivation(
    seed: Annotated[SeedBody, Query()],
    derivation: DerivationType,
) -> Keypair:
    hdwallet: BIP32HD = await internal_bip32_derivation(seed.seed, derivation)
    return Keypair(pubkey=hdwallet.xpublic_key(), prvkey=hdwallet.xprivate_key())


@router.post(
    "/from_derivation/",
    summary="Generate a keypair from a BIP32 derivation path",
    response_description="A public/private key pair",
)
async def post_bip32_derivation(payload: DerivationBody) -> Keypair:
    seed = payload.seed
    derivation = payload.derivation
    hdwallet: BIP32HD = await internal_bip32_derivation(seed, derivation)
    return Keypair(pubkey=hdwallet.xpublic_key(), prvkey=hdwallet.xprivate_key())

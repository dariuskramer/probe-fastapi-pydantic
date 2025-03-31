from typing import Annotated, ClassVar
from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field
from hdwallet.derivations import CustomDerivation
from hdwallet.hds import BIP32HD
from hdwallet.cryptocurrencies import Bitcoin

router = APIRouter(prefix="/hdwallet")


# @router.get("/derivation/{derivation:path}")
# async def derivation(seed: Annotated[str, Body()], derivation: str = "m"):
#     pass


class PostBip32Req(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid")
    seed: Annotated[
        str, Field(min_length=32, max_length=128, pattern=r"^[0-9A-Fa-f]+$")
    ]
    derivation: Annotated[str, Field(min_length=1, pattern=r"^m(/\d+'?)*$")] = "m"


@router.post("/derivation/")
async def bip32_derivation(payload: PostBip32Req):
    hdwallet: BIP32HD = (
        BIP32HD(ecc=Bitcoin.ECC)
        .from_seed(payload.seed)
        .from_derivation(CustomDerivation(payload.derivation))
    )
    return {"pubkey": hdwallet.xpublic_key(), "prvkey": hdwallet.xprivate_key()}

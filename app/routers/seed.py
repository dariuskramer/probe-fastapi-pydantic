from typing import Annotated
from fastapi import APIRouter, Body
from hdwallet.entropies.bip39 import BIP39Entropy
from hdwallet.mnemonics.bip39 import BIP39Mnemonic, BIP39_MNEMONIC_LANGUAGES
from hdwallet.seeds.bip39 import BIP39Seed
from pydantic import AfterValidator, BaseModel

from app.routers import HEXADECIMAL_PATTERN, SeedType

router = APIRouter(prefix="/seed")


def check_wordlist(mnemonic: str) -> str:
    words: list[str] = mnemonic.split("/")
    if BIP39Mnemonic.is_valid(words):
        return mnemonic
    raise ValueError(f"mnemonic is not valid: {mnemonic}")


@router.get("/from_words/{mnemonic:path}")
async def get_seed_from_words(
    mnemonic: Annotated[str, AfterValidator(check_wordlist)],
):
    words = mnemonic.replace("/", " ")
    bip39_mnemonic: BIP39Mnemonic = BIP39Mnemonic(mnemonic=words)
    bip39_seed: str = BIP39Seed.from_mnemonic(
        mnemonic=bip39_mnemonic,
        passphrase="TREZOR",  # configured to use test vectors from BIP39
    )

    return {
        "entropy": bip39_mnemonic.decode(words),
        "mnemonic": bip39_mnemonic.mnemonic().split(),
        "seed": bip39_seed,
    }


class Entropy(BaseModel):
    entropy: Annotated[
        str, Body(min_length=32, max_length=64, pattern=HEXADECIMAL_PATTERN)
    ]


@router.post("/from_entropy/")
async def get_seed_from_entropy(entropy: Entropy):
    bip39_entropy: BIP39Entropy = BIP39Entropy(entropy=entropy.entropy)
    bip39_mnemonic: str = BIP39Mnemonic.from_entropy(
        bip39_entropy, BIP39_MNEMONIC_LANGUAGES.ENGLISH
    )
    bip39_seed: str = BIP39Seed.from_mnemonic(
        mnemonic=bip39_mnemonic,
        passphrase="TREZOR",  # configured to use test vectors from BIP39
    )

    return {
        "entropy": bip39_entropy.entropy(),
        "mnemonic": bip39_mnemonic.split(),
        "seed": bip39_seed,
    }

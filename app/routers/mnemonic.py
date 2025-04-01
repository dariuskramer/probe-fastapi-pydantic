from typing import Annotated
from fastapi import APIRouter
from hdwallet.mnemonics.bip39 import BIP39Mnemonic
from hdwallet.seeds.bip39 import BIP39Seed
from pydantic import AfterValidator

router = APIRouter(prefix="/mnemonic")


def check_wordlist(mnemonic: str) -> str:
    words: list[str] = mnemonic.split("/")
    if BIP39Mnemonic.is_valid(words):
        return mnemonic
    raise ValueError(f"mnemonic is not valid: {mnemonic}")


@router.get("/{mnemonic:path}")
async def get_mnemonic_seed(
    mnemonic: Annotated[str, AfterValidator(check_wordlist)],
):
    words = mnemonic.replace("/", " ")
    bip39_mnemonic: BIP39Mnemonic = BIP39Mnemonic(mnemonic=words)
    bip39_seed: str = BIP39Seed.from_mnemonic(
        mnemonic=bip39_mnemonic,
        passphrase="TREZOR",  # configured to use test vectors from BIP39
    )

    return {
        "mnemonic": bip39_mnemonic.mnemonic().split(),
        "seed": bip39_seed,
        "entropy": bip39_mnemonic.decode(words),
    }

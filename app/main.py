from fastapi import FastAPI

from .routers import entropy, hdwallet, mnemonic

app = FastAPI()


app.include_router(entropy.router)
app.include_router(mnemonic.router)
app.include_router(hdwallet.router)

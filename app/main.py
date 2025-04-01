from fastapi import FastAPI

from .routers import hdwallet, mnemonic

app = FastAPI()


app.include_router(hdwallet.router)
app.include_router(mnemonic.router)

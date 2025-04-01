from fastapi import FastAPI

from .routers import entropy, seed, hdwallet

app = FastAPI()


app.include_router(entropy.router)
app.include_router(seed.router)
app.include_router(hdwallet.router)

from fastapi import FastAPI

from .routers import entropy, seed, keypair

app = FastAPI()


app.include_router(entropy.router)
app.include_router(seed.router)
app.include_router(keypair.router)

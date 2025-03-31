from fastapi import FastAPI

from .routers import hdwallet

app = FastAPI()


app.include_router(hdwallet.router)

import utils

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/start", response_class=PlainTextResponse)
async def healthCheck() -> str:
    return "ok"

@app.get("/help", response_class=PlainTextResponse)
async def sendHelp(payload: str) -> str:
    return utils.help(payload)

@app.get("/uwu", response_class=PlainTextResponse)
async def uwu(payload: str) -> str:
    return utils.uwu(payload)
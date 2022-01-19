import utils

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/start", response_class=PlainTextResponse)
async def healthCheck() -> str:
    return "ok"

@app.get("/help", response_class=PlainTextResponse)
async def sendHelp(content: str) -> str:
    return utils.help(content)

@app.get("/uwu", response_class=PlainTextResponse)
async def uwu(content: str) -> str:
    return utils.uwuify(content)

@app.get("/kaannos", response_class=PlainTextResponse)
async def kaannos(content: str, modifier: int = 1) -> str:
    return utils.misspell(content, modifier)

from typing import Optional
import utils

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse



app = FastAPI()

@app.get("/start", response_class=PlainTextResponse)
async def healthCheck() -> str:
    return "ok"

@app.get("/help", response_class=PlainTextResponse)
async def help(text: str) -> str:
    return utils.help(text)

@app.get("/uwu", response_class=PlainTextResponse)
async def uwu(text: Optional[str] = "") -> str:
    return utils.uwuify(text)

@app.get("/kaannos", response_class=PlainTextResponse)
async def kaannos(text: str, level: Optional[int] = 1) -> str:
    if not 1 <= level <= 10:
        return "Syötä kännin taso väliltä 1-10"
    else:
        return utils.misspell(text, level)

@app.get("/meme", response_class=PlainTextResponse)
async def getMeme() -> str:
    return utils.getMeme()
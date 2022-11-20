from JSONLParser import JSONLParser
from config import *
from datetime import date
from Cleanaer import Cleaner
import restApi as API
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

parser = JSONLParser(DATA_INFO_SOURCE_PATH)
cleaner = Cleaner(parser)
cleaner.cleanAndStoreData()
cleaner.getExchangeRate(EXCHANGE_INFO_SOURCE_PATH)


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/userLevel")
async def get_user_level_stats(user_id:str, date:date=None):
    ret = API.userStats(user_id, date)
    if not ret:
        return {"message": 'error, wrong user_id or date'}
    return JSONResponse(content=jsonable_encoder(ret))


@app.get("/api/gameLevel")
async def get_game_level_stats(date:date=None):
    ret = API.gameStats(date, None)
    if not ret:
        return {"message": 'error, wrong date'}
    return JSONResponse(content=jsonable_encoder(ret))

@app.get("/api/gameLevel/country")
async def get_game_level_stats_country(date:date=None):
    ret = API.gameStats(date, True)
    if not ret:
        return {"message": 'error, wrong user_id or date'}
    return JSONResponse(content=jsonable_encoder(ret))


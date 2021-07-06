from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
import crud
from model import CurrencyExchgeRate
from datetime import date
from pymongo import errors

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def get_version():
    return """
     <html>
        <head>
            <title>Currency rates</title>
        </head>
        <body>
            <a href="http://localhost:8000/docs">openapi.json</a></p>
            <a href="http://localhost:8000/redoc">ReDoc</a></p>
        </body>
    </html>
"""

@app.get("/exch_rate/{currencyCode}")
async def get_rates(*, currencyCode: str = Path(..., max_length = 3, min_length = 3,  example = 'EUR'), from_date: date, to_date: date, skip: int = 0, limit: int = 30):
    result =  await crud.read_cur_rate_period(currencyCode, from_date, to_date, skip, limit)
    return result

@app.get("/exch_rate/{currencyCode}/{date}")
async def get_rate_as_of_date(*, currencyCode: str = Path(..., max_length = 3, min_length = 3,  example = 'EUR'), date: date):
    result = await crud.read_cur_rate_as_of_date(currencyCode, date)
    return result

@app.post("/exch_rate")
async def add_exch_rate(currency_exchge_rate: CurrencyExchgeRate):
    try :
        result = await crud.add_cur_rate(jsonable_encoder(currency_exchge_rate))
    except errors.DuplicateKeyError:
        raise HTTPException(status_code=409 , detail="The record already exists") 
    return result

@app.put("/exch_rate")
async def update(currency_exchge_rate: CurrencyExchgeRate):    
    result = await crud.update_cur_rate(jsonable_encoder(currency_exchge_rate))
    return result

@app.delete("/exch_rate/{currencyCode}/{date}")
async def delete_on_date(*, currencyCode: str = Path(..., max_length = 3, min_length = 3,  example = 'EUR'), onDate: date):
    result  = await crud.delete_currency_rate_on_date(currencyCode, onDate)
    return result

@app.delete("/exch_rate/{currencyCode}")
async def delete_period(*, currencyCode: str  = Path(..., max_length = 3, min_length = 3,  example = 'EUR'), fromDate: date, toDate: date):
    result  = await crud.delete_currency_rate_period(currencyCode, fromDate, toDate)
    return result  

@app.delete("/exch_rate/{currencyCode}/deleteAll/")
async def delete_whole_currency(currencyCode: str = Path(..., max_length = 3, min_length = 3,  example = 'EUR')):
    result  = await crud.delete_whole_currency(currencyCode)
    return result         




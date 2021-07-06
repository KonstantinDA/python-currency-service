from enum import unique
import motor.motor_asyncio
import pymongo
import model
import json 
from datetime import date


client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://mongo_user:mongo_password@mongo:27017')

db = client.currency

db_collection_rate = db.exchangeRate
db_collection_rate.create_index([('code', pymongo.ASCENDING), ('date', pymongo.ASCENDING)], unique=True)


async def add_cur_rate(exch_rate_json):
    insertResult =  await db_collection_rate.insert_one(exch_rate_json)    
    new_document = await db_collection_rate.find_one({"_id": insertResult.inserted_id}, {"_id":0})
    new_document_json = json.dumps(new_document, indent  = 4)
    return model.CurrencyExchgeRate.parse_raw(new_document_json)

async def read_cur_rate_as_of_date(currencyCode: str, on_date: date):
    document = await db_collection_rate.find_one({"code": currencyCode, "date": date.isoformat(on_date)}, {"_id":0}) 
    if (document is not None) :
        document_json = json.dumps(document, indent  = 4)
        currency_exchge_rate =  model.CurrencyExchgeRate.parse_raw(document_json)
        return currency_exchge_rate
    else :
        return None

async def read_cur_rate_period(currencyCode: str, from_date: date, to_date: date, skip: int = 0, limit: int = 30):
    cursor = db_collection_rate.find({"code": currencyCode, "date": {"$gte": date.isoformat(from_date), "$lte": date.isoformat(to_date)}}, {"_id":0}).sort("date").skip(skip).limit(limit)
    currency_exchge_rates = []
    for document in await cursor.to_list(length = limit):    
        document_json = json.dumps(document, indent  = 4)
        currency_exchge_rate =  model.CurrencyExchgeRate.parse_raw(document_json)
        currency_exchge_rates.append(currency_exchge_rate)
    return currency_exchge_rates

async def update_cur_rate(exch_rate_json):    
    result = await db_collection_rate.replace_one({'code': exch_rate_json["code"], "date": exch_rate_json["date"]}, exch_rate_json)
    if result.modified_count :
        updated_document = await db_collection_rate.find_one({"code": exch_rate_json["code"], "date": exch_rate_json["date"]}, {"_id":0}) 
        if (updated_document is not None) :
            updated_document_json = json.dumps(updated_document, indent  = 4)
            currency_exchge_rate_updated =  model.CurrencyExchgeRate.parse_raw(updated_document_json)
            return currency_exchge_rate_updated
        else :
            return None        

    return 

async def delete_whole_currency(currencyCode: str):
    result = await db_collection_rate.delete_many({'code': currencyCode})
    return {"deletedRecordsCount":result.deleted_count}

async def delete_currency_rate_period(currencyCode: str, from_date: date, to_date: date):
    result = await db_collection_rate.delete_many({'code': currencyCode, "date": {"$gte": date.isoformat(from_date), "$lte": date.isoformat(to_date)}})
    return {"deletedRecordsCount":result.deleted_count}    

async def delete_currency_rate_on_date(currencyCode, onDate):
    result = await db_collection_rate.delete_one({'code': currencyCode, "date": date.isoformat(onDate)})
    return {"deletedRecordsCount":result.deleted_count}





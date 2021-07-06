from pydantic import BaseModel, validator
from datetime import date
from enum import Enum

class exchange_units(Enum):
    per_1 = 1
    per_10 = 10
    per_100 = 100
    per_1000 = 1000
    per_10000 = 10000

class CurrencyExchgeRate(BaseModel):
    code: str
    date: date
    unit: exchange_units
    value: float    
    value_open: float = 0  # is not mandatory
    value_close: float = 0 # is not mandatory
    value_min: float = 0 # is not mandatory
    value_max:float = 0 # is not mandatory

    @validator('code')
    def code_len(cls, v) :
        if len(v) != 3 :
            raise ValueError('The Currency code must contain three chars')
        return v
  
    @validator('value') 
    def value_positive(cls, v) : 
        if v < 0:
            raise ValueError('The Value must be a positive')
        return v

    @validator('value_open') 
    def value_open_positive(cls, v) : 
        if v < 0:
            raise ValueError('The Value must be a positive')
        return v

    @validator('value_close') 
    def value_close_positive(cls, v) : 
        if v < 0:
            raise ValueError('The Value must be a positive')
        return v        

    @validator('value_min') 
    def value_min_positive(cls, v) : 
        if v < 0:
            raise ValueError('The Value must be a positive')
        return v

    @validator('value_max') 
    def value_max_positive(cls, v) : 
        if v < 0:
            raise ValueError('The Value must be a positive')
        return v          
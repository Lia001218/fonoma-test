
import logging
from fastapi import FastAPI, Query, Body
from typing import Annotated
from pydantic import BaseModel
from enum import Enum
import redis
import os 

endpoint = os.environ.get("REDIS_URL") or 'localhost'
app = FastAPI()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
redis_client = redis.StrictRedis(host=endpoint, port=6379)

class StatusModel(str,Enum):
    completed = "completed"
    pending = "pending"
    canceled = "canceled"

class CriterionEnum(str, Enum):
    completed = "completed"
    pending = "pending"
    canceled = "canceled"
    all      =  "all"

class Order(BaseModel):
    id: int
    item : str
    quantity: int 
    price: Annotated[float, Query(ge = 0)]
    status: StatusModel

    def __hash__(self) -> int:
        return hash((self.id, self.item, self.quantity, self.price, self.status))

@app.post("/solution")
def process_orders(orders : list[Order] , criterion : Annotated[CriterionEnum, Body()]):
    log.info('processing post')
    cache_key = f"{criterion.value}:{hash(tuple(orders))}"
    
    cached_result = redis_client.get(cache_key)
    if cached_result:
        log.info('Cache hit')
        return float(cached_result)
    if criterion == CriterionEnum.all:
        result = sum(x.price * x.quantity for x in orders)
    else: 
        result = sum(x.price * x.quantity for x in filter(lambda x: x.status == criterion, orders))
    
    redis_client.setex(cache_key, 3600, str(result))
    return result


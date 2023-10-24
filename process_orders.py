from fastapi import FastAPI, Query, Body
from typing import Annotated
from pydantic import BaseModel
from enum import Enum

app = FastAPI()


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


@app.post("/solution")
def process_orders(orders : list[Order] , criterion : Annotated[CriterionEnum, Body()]):
    if criterion == CriterionEnum.all:
        return sum(x.price * x.quantity for x in orders)
    return sum(x.price * x.quantity for x in filter(lambda x: x.status == criterion, orders))
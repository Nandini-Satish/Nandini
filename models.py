from pydantic import BaseModel
from datetime import datetime


class Item(BaseModel):
    name: str
    email: str
    item_name: str
    quantity: int
    expiry_date: str


class ClockInRecord(BaseModel):
    email: str
    location: str


# Helper to convert ObjectId to str
class ItemInDB(Item):
    id: str
    insert_date: datetime


class ClockInRecordInDB(ClockInRecord):
    id: int
    insert_datetime: datetime

from fastapi import APIRouter, HTTPException
from datetime import datetime
from bson import ObjectId
from typing import List, Optional
from models import ClockInRecord
from database import db
router = APIRouter()


# POST /clock-in
@router.post("/clock-in", response_model=ClockInRecord)
async def create_clock_in(record: ClockInRecord):
    insert_datetime = datetime.now()
    new_record = {
        "email": record.email,
        "location": record.location,
        "insert_datetime": insert_datetime,
    }
    result = await db.clock_in.insert_one(new_record)
    new_record["id"] = str(result.inserted_id)
    return ClockInRecord(**new_record)


# GET /clock-in/{id}
@router.get("/clock-in/{id}", response_model=ClockInRecord)
async def get_clock_in(id: str):
    record = await db.clock_in.find_one({"_id": ObjectId(id)})
    if record is None:
        raise HTTPException(
            status_code=404, detail="Clock-in record not found")
    record["id"] = str(record["_id"])
    return ClockInRecord(**record)


# GET /clock-in/filter
@router.get("/clock-in/filter", response_model=List[ClockInRecord])
async def filter_clock_ins(
    email: Optional[str] = None,
    location: Optional[str] = None,
    after_datetime: Optional[datetime] = None
):
    query = {}
    if email:
        query["email"] = email
    if location:
        query["location"] = location
    if after_datetime:
        query["insert_datetime"] = {"$gt": after_datetime}

    records = await db.clock_in.find(query).to_list(length=100)
    for record in records:
        record["id"] = str(record["_id"])
    return [ClockInRecord(**record) for record in records]


# DELETE /clock-in/{id}
@router.delete("/clock-in/{id}")
async def delete_clock_in(id: str):
    result = await db.clock_in.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404, detail="Clock-in record not found")
    return {"detail": "Clock-in record deleted"}


# PUT /clock-in/{id}
@router.put("/clock-in/{id}", response_model=ClockInRecord)
async def update_clock_in(id: str, record: ClockInRecord):
    update_data = {k: v for k, v in record.dict().items() if k != "id"}
    result = await db.clock_in.update_one(
        {"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(
            status_code=404, detail="Clock-in record not found")
    updated_record = await db.clock_in.find_one({"_id": ObjectId(id)})
    updated_record["id"] = str(updated_record["_id"])
    return ClockInRecord(**updated_record)

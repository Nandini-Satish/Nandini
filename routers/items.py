from typing import Optional
from fastapi import APIRouter, HTTPException, status
from models import Item, ItemInDB
from database import items_collection
from bson import ObjectId
from datetime import datetime
import logging

router = APIRouter()


@router.post("/items", response_model=ItemInDB, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    new_item = {
        "name": item.name,
        "email": item.email,
        "item_name": item.item_name,
        "quantity": item.quantity,
        "expiry_date": item.expiry_date,
        "insert_date": datetime.utcnow(),  # Add UTC insert date
    }

    try:
        # Insert the new item into MongoDB
        result = await items_collection.insert_one(new_item)

        # Prepare the response model with the inserted ID
        item_in_db = ItemInDB(**new_item, id=str(result.inserted_id))
        return item_in_db
    except Exception as e:
        logging.error(f"Failed to create item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not create item. Error: {str(e)}"
        )


# GET: Retrieve Item by ID
@router.get("/items/{id}", response_model=ItemInDB)
async def get_item(id: str):
    try:
        item = await items_collection.find_one({"_id": ObjectId(id)})
        if item:
            item["id"] = str(item["_id"])
            return item
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        logging.error(f"Failed to retrieve item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid item ID format."
        )


# GET: Filter Items
@router.get("/items/filter")
async def filter_items(
    email: Optional[str] = None,
    expiry_date: Optional[datetime] = None,
    insert_date: Optional[datetime] = None,
    quantity: Optional[int] = None
):
    query = {}
    if email:
        query["email"] = email
    if expiry_date:
        query["expiry_date"] = {"$gt": expiry_date}
    if insert_date:
        query["insert_date"] = {"$gt": insert_date}
    if quantity is not None:
        query["quantity"] = quantity

    items = await items_collection.find(query).to_list(length=100)
    for item in items:
        item["id"] = str(item["_id"])
    return items


# DELETE: Delete Item by ID
@router.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(id: str):
    result = await items_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"detail": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")


# PUT: Update Item by ID
@router.put("/items/{id}", response_model=ItemInDB)
async def update_item(id: str, item: Item):
    try:
        updated_item = await items_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": item.dict(exclude_unset=True)},
            return_document=True
        )
        if updated_item:
            updated_item["id"] = str(updated_item["_id"])
            return updated_item
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        logging.error(f"Failed to update item: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data format.")


# GET: Aggregate Items by Email
@router.get("/items/aggregate/email")
async def aggregate_items_by_email():
    pipeline = [
        {
            "$group": {
                "_id": "$email",
                "count": {"$sum": 1}
            }
        }
    ]
    result = await items_collection.aggregate(pipeline).to_list(length=100)
    return result

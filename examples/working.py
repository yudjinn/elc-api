from fastapi import FastAPI, Path, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


inventory = {}


@app.get("/get-item/{item_id}")
def get_item(
    item_id: int = Path(None, description="The ID of the item you'd like to view", gt=0)
):
    return inventory.get(item_id)


@app.get("/get-by-name")
def get_by_name(name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Item Found By That Name.",
            )


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"Error": "Item id already in use."}

    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in inventory:
        return {"Error": "Item id does not exist."}

    inventory[item_id].update(item)
    return inventory[item_id]

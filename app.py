from typing import Optional
import json
import os
from fastapi import FastAPI
from pydantic import BaseModel

# Simple python application

file_path = os.path.join(os.path.dirname(__file__), 'items.json')
app = FastAPI()

class Item(BaseModel):
  id: Optional[int] = None
  nom: str
  prix: float


with open(file_path, 'r') as f:
  items = json.load(f)



@app.get("/")
def read_root():
  return {"Hello ": "From my Kubernetes App side"}


@app.get("/items/")
def get_items():
  return json.dumps(items)


@app.post("/items/")
def create_item(item: Item):
  # user did not specify id in the post or it already exist
  if item.id is None or item.id in [existing_item['id'] for existing_item in items]:
    item_id = max([p['id'] for p in items]) + 1
  else:
    item_id = item.id

  new_item = {"id": item_id, "nom": item.nom, "prix": item.prix}
  items.append(new_item)
  with open('items.json', 'w') as f:
    json.dump(items, f)
  return new_item


@app.get("/items/{item_id}")
def get_item(item_id: int):
  item = [i for i in items if i['id'] == item_id]
  return item[0] if len(item) > 0 else {}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
  for i, db_item in enumerate(items):
    if db_item["id"] == item_id:
      items[i] = item.dict()
      with open('items.json', 'w') as f:
        json.dump(items, f)
      return {"message": "Produit ajouté"}
  return {"message": "Dommage. Produit non trouvé"}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
  for i, item in enumerate(items):
    if item["id"] == item_id:
      items.pop(i)
      with open('items.json', 'w') as f:
        json.dump(items, f)
      return {"message": "Produit supprimé correctement."}
  return {"message": "Produit non trouvé."}

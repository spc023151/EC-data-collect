from typing import Optional
from fastapi import FastAPI
import pandas as pd
from sqlalchemy import create_engine

app = FastAPI()

engine = create_engine('postgresql://postgres:6nnr87ac@localhost:5432/ruten')

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def item(item_id: str):
    item_id = item_id.split(",")
    if(len(item_id)>50):
        return None
        
    df = pd.read_sql('SELECT * FROM item_detail where "ProdId" in ({})'.format("\'"+"\',\'".join(item_id)+"\'"), engine)

    return df.to_json(orient="records")

@app.get("/catg/{catg_id}")
def item(catg_id: str):
    df = pd.read_sql('SELECT "ProdId" FROM item_detail where "CateId" = \'{}\''.format(catg_id), engine)
    return df.to_json(orient="records")

@app.get("/items")
def items_param(offset: int, limit: int):
    df = pd.read_sql('SELECT * FROM item_detail limit {} offset {}'.format(limit, offset), engine)
    
    return df.iloc[offset:offset+limit].to_json(orient="records")
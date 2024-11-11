import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Any
import json
from pydantic import BaseModel

class PrettyJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return json.dumps(content, ensure_ascii=False, indent=4).encode("utf-8")

class Car(BaseModel):
    brand: str
    model: str
    transmission: str
    age: float
    fuel: str
    engine: float
    km: float
    owner: float
    price: float
    location: str
    mileage: float
    power: float
    seats: float
    type: str

carList = pd.read_csv(r'C:\Users\nicke\Desktop\Reps\ApiPanda\carsale.csv')
carList.fillna('No Data', inplace=True)

app = FastAPI(default_response_class=PrettyJSONResponse)

@app.get("/get-message")
async def read_root():
    return {"message": "WASSAAAAAAAAAAAAAAAAAAAAAAAA"}

@app.get("/get-car-list")
async def get_car_list():
    return carList.to_dict(orient='records')

@app.get("/get-car-columns")
async def get_car_columns(column: str):
    if column in carList.columns:
        filtered_data = carList[carList[column] != 'No Data']
        return filtered_data[column].to_dict()
    else:
        return {"error": "Column not found"}

@app.get("/get-car-by-brand-and-model")
async def get_car_by_brand_and_model(brand: str, model: str):
    filtered_data = carList[(carList['brand'] == brand) & (carList['model'] == model)]
    return filtered_data.to_dict(orient='records')

@app.post("/add-car")
async def add_car(car: Car):
    new_row = {col: getattr(car, col, " ") for col in carList.columns}
    if all(value == " " for value in new_row.values()):
        return {"error": "Cannot add an empty car entry"}
    carList.loc[len(carList)] = new_row
    return {"message": "Car added successfully"}

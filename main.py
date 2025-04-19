from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Optional, List
from pydantic import BaseModel
import cost_of_living

# Define response models
class CityCostOfLiving(BaseModel):
    city: str
    cost_of_living_index: float
    rent_index: float
    cost_of_living_plus_rent_index: float
    groceries_index: float
    restaurant_price_index: float
    local_purchasing_power_index: float

class Message(BaseModel):
    message: str

class PopulateResponse(BaseModel):
    status: str
    message: str

app = FastAPI(
    title="Cost of Living API",
    description="""
    An API providing cost of living data for cities worldwide.
    Data source: Your cost of living dataset
    """,
    version="1.0.0",
    contact={
        "name": "Cost of Living API Team",
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
)

@app.get("/", response_model=Message, tags=["General"])
async def root():
    """Welcome endpoint for the Cost of Living API."""
    return {"message": "Welcome to the Cost of Living API"}

@app.post("/populate", response_model=PopulateResponse, tags=["Data"])
async def populate():
    """Populate the database with cost of living data."""
    try:
        cost_of_living.populate()
        return {"status": "success", "message": "Data populated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/city/{city_name}", response_model=CityCostOfLiving, tags=["Cities"])
async def get_city_cost(city_name: str):
    """
    Get cost of living data for a specific city.
    
    Parameters:
        city_name (str): Name of the city to look up (e.g., 'Hamilton, Bermuda')
        
    Returns:
        CityCostOfLiving: Cost of living details for the specified city
    """
    try:
        result = cost_of_living.get_city_data(city_name)
        if result is None:
            raise HTTPException(status_code=404, detail="City not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/most-expensive-cities", response_model=List[CityCostOfLiving], tags=["Cities"])
async def get_most_expensive_cities(limit: Optional[int] = 10):
    """
    Get the most expensive cities by cost of living index.
    
    Parameters:
        limit (int, optional): Number of cities to return. Defaults to 10.
    """
    try:
        return cost_of_living.get_most_expensive_cities(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cheapest-cities", response_model=List[CityCostOfLiving], tags=["Cities"])
async def get_cheapest_cities(limit: Optional[int] = 10):
    """
    Get the cheapest cities by cost of living index.
    
    Parameters:
        limit (int, optional): Number of cities to return. Defaults to 10.
    """
    try:
        return cost_of_living.get_cheapest_cities(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/best-value-cities", response_model=List[CityCostOfLiving], tags=["Cities"])
async def get_best_value_cities(limit: Optional[int] = 10):
    """
    Get cities with the best value (highest local purchasing power relative to cost).
    
    Parameters:
        limit (int, optional): Number of cities to return. Defaults to 10.
    """
    try:
        return cost_of_living.get_best_value_cities(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
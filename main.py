from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="Customer API", version="1.0.0")

# In-memory storage (replace with database in production)
customers_db = []
customer_id_counter = 1


class Customer(BaseModel):
    id: int = None
    name: str
    email: str
    phone: str = None
    created_at: datetime = None

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0"
    }


@app.post("/customers", response_model=Customer)
async def add_customer(customer: Customer):
    """Add a new customer"""
    global customer_id_counter

    if not customer.name or not customer.email:
        raise HTTPException(status_code=400, detail="Name and email are required")

    customer.id = customer_id_counter
    customer.created_at = datetime.now()
    customer_id_counter += 1

    customers_db.append(customer.dict())
    return customer


@app.get("/customers", response_model=List[Customer])
async def list_customers():
    """List all customers"""
    return customers_db


@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    """Get a specific customer by ID"""
    for customer in customers_db:
        if customer["id"] == customer_id:
            return customer
    raise HTTPException(status_code=404, detail="Customer not found")


@app.put("/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, customer_update: Customer):
    """Update a customer"""
    for i, customer in enumerate(customers_db):
        if customer["id"] == customer_id:
            updated_data = customer_update.dict(exclude_unset=True)
            customers_db[i].update(updated_data)
            return customers_db[i]
    raise HTTPException(status_code=404, detail="Customer not found")


@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int):
    """Delete a customer"""
    global customers_db
    for i, customer in enumerate(customers_db):
        if customer["id"] == customer_id:
            customers_db.pop(i)
            return {"message": "Customer deleted successfully"}
    raise HTTPException(status_code=404, detail="Customer not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

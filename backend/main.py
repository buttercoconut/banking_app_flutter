from fastapi import FastAPI
from app.routes.deposits import router as deposits_router
from app.database import engine, Base

app = FastAPI(title="Banking Deposit Service")

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(deposits_router, prefix="/api/v1/deposits", tags=["Deposits"])

@app.on_event("startup")
async def startup_event():
    # Placeholder for any startup tasks
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Placeholder for any shutdown tasks
    pass

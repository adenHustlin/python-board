from fastapi import FastAPI

from app.api.v1.account import router as account_router

app = FastAPI()

# Include routers
app.include_router(account_router, prefix="/account", tags=["account"])

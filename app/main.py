from fastapi import FastAPI

from app.api.v1.account import router as account_router
from app.api.v1.board import router as board_router
from app.api.v1.post import router as post_router

app = FastAPI()


# Include routers
app.include_router(account_router, prefix="/api/v1", tags=["account"])
app.include_router(board_router, prefix="/api/v1", tags=["board"])
app.include_router(post_router, prefix="/api/v1", tags=["post"])

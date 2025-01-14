from fastapi import FastAPI, Request
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Auth System", version="1.0.0")

app.include_router(auth_router, prefix="/api/v1/users")
app.include_router(user_router, prefix="/api/v1/users")

@app.middleware("http")
async def log_request_headers(request: Request, call_next):
    print("Authorization Header:", request.headers.get("authorization"))
    return await call_next(request)


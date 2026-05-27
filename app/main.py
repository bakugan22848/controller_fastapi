import uvicorn
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.routers.healthcheck import router as healthcheck_router
from app.routers.user_routers import router as user_router
from app.routers.device_routers import router as device_router
from app.routers.trigger_routers import router as trigger_router
from app.routers.controller_routers import router as controller_router
from app.routers.auth_routers import router as auth_router
from app.routers.admin_routers import router as admin_router
from app.routers.esp_routers import router as esp_router

from app.core.config import settings as stt
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

app.include_router(healthcheck_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(trigger_router)
app.include_router(controller_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(esp_router)

if __name__ == "__main__":
    uvicorn.run("main.py:app", host=stt.HOST, port=stt.PORT, reload=True)
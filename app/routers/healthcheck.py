from fastapi import HTTPException, APIRouter
from sqlalchemy import text

from app.routers.dependencies import session_dep
#from app.database.redis import get_redis

#redis_db = get_redis()

router = APIRouter(
    tags=["HealthCheck"],
)

@router.get("/")
def healthcheck():
    return {"status_code": 200,
            "detail": "ok",
            "result": "working"}

@router.get("/db")
async def check_db(session: session_dep):
    try:
        result = await session.execute(text('SELECT current_database();'))
        return {"status_code": 200, "detail": f"Database connected", "db_name":f"{result.scalar()}"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database connection failed: {e}")
    finally:
        await session.close()
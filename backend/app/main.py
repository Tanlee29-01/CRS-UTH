from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import time

from app.api.router import api_router
from app.core.config import settings


app = FastAPI(title=settings.app_name)

_rate_state = {}


@app.middleware("http")
async def rate_limit(request: Request, call_next):
    key = request.client.host if request.client else "unknown"
    now = time.time()
    window = 60
    state = _rate_state.get(key, [])
    state = [t for t in state if now - t < window]
    if len(state) >= settings.rate_limit_per_minute:
        return Response(status_code=429, content="Too Many Requests")
    state.append(now)
    _rate_state[key] = state
    return await call_next(request)

origins = [o.strip() for o in settings.frontend_origin.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

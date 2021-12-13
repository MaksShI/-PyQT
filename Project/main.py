from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import settings
from api.api_v1.api import api_router

app = FastAPI(
    title='Messenger', openapi_url=f"127.0.0.1/api/v1/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

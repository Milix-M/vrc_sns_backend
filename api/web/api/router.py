from fastapi.routing import APIRouter

from api.web.api import auth, users, token
from api.web.api.auth import google

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(token.router)
api_router.include_router(google.router, prefix="/google", tags=["GoogleAuth"])
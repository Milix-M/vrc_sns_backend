from fastapi import FastAPI

from api.web.api.router import api_router
from api.web.lifetime import register_startup_event, register_shutdown_event

def get_app() -> FastAPI:
    """
    Get FastAPI application.
    """

    app = FastAPI()

    #スタートアップ/シャットダウン時のイベントを追加
    register_startup_event(app)
    register_shutdown_event(app)

    app.include_router(router=api_router, prefix="/api")

    return app
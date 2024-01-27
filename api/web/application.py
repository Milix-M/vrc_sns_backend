from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.web.api.router import api_router
from api.web.lifetime import register_startup_event, register_shutdown_event
from api.settings import settings

def get_app() -> FastAPI:
    """
    Get FastAPI application.
    """

    app = FastAPI()

    #スタートアップ/シャットダウン時のイベントを追加
    register_startup_event(app)
    register_shutdown_event(app)

    app.include_router(router=api_router, prefix="/api")
    app.add_middleware(
        CORSMiddleware,
        #許可するオリジンを指定
        allow_origins=settings.origins,
        #認証情報のアクセスを許可
        allow_credentials=True,
        # 全てのリクエストメソッドを許可
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
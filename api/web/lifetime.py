from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.settings import settings

def _setup_db(app: FastAPI) -> None:
    """
    Creates connection to the database.

    This function creates SQLAlchemy engine instance

    :param app: fastAPI application.
    """
    engine =create_async_engine(str(settings.db_url), future=True, echo=settings.db_echo)
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit = False,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


def register_startup_event(app: FastAPI):
    @app.on_event("startup")
    async def _startup() -> None:
        _setup_db(app)
        pass

    return _startup

def register_shutdown_event(app: FastAPI):
    @app.on_event("shutdown")
    async def _shutdown() -> None:
        await app.state.db_engine.dispose()
        pass

    return _shutdown
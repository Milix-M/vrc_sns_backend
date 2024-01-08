import uvicorn

from api.settings import settings

def main() -> None:
    """Entrypoint of the app"""
    if settings.reload:
        uvicorn.run(
            "api.web.application:get_app",
            host=settings.host,
            port=settings.port,
            reload=settings.reload,
            factory=True
        )

if __name__ == "__main__":
    main()
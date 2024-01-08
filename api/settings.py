class Settings():
    """
    Application Settings.
    """
    host : str = "127.0.0.1"
    port : int = 8000
    reload: bool = True

    db_url: str = "sqlite:///sns_app.db"



settings = Settings()
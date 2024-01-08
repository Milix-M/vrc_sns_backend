class Settings():
    """
    Application Settings.
    """
    db_url: str = "sqlite:///sns_app.db"
    reload: bool = True


settings = Settings()
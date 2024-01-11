from yarl import URL

class Settings():
    """
    Application Settings.
    """
    host : str = "0.0.0.0"
    port : int = 8000
    reload: bool = True

    db_host = "db"
    db_port = 5432
    db_user = "postgres"
    db_pass = "password"
    db_base = "app"
    db_echo = True


    # token credentials
    token_algorithm: str = "HS512"
    token_secret_key: str ="add_some_secret_key"

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )


settings = Settings()
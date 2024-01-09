from yarl import URL

class Settings():
    """
    Application Settings.
    """
    host : str = "127.0.0.1"
    port : int = 8000
    reload: bool = True

    db_host = "db"
    db_port = 5432
    db_user = "postgres"
    db_pass = "password"
    db_base = "app"
    db_echo = True

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="sqlite+aiosqlite",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )


settings = Settings()
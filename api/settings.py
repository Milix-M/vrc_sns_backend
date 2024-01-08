from yarl import URL

class Settings():
    """
    Application Settings.
    """
    host : str = "127.0.0.1"
    port : int = 8000
    reload: bool = True

    db_host = ""
    db_port = 0
    db_user = ""
    db_pass = ""
    db_base = "//sns_app.db"
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
from yarl import URL
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Settings():
    """
    Application Settings.
    """
    web_url: str = "http://127.0.0.1:3000"

    domain: str = "localhost"
    host : str = "0.0.0.0"
    port : int = 8000
    reload: bool = True

    db_host = "db"
    db_port = 5432
    db_user = "postgres"
    db_pass = "password"
    db_base = "app"
    db_echo = True

    is_production = False

    # token credentials
    token_algorithm: str = "HS512"
    token_secret_key: str ="add_some_secret_key"

    #OAuth credentials
    google_client_id = os.environ.get("GOOGLE_CLIENT_ID")
    google_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

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
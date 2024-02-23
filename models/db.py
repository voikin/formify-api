from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from configs.config import SingletonSettings

settings = SingletonSettings()


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )


db = DatabaseHelper(url=settings.db.url, echo=settings.db.echo)

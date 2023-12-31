import logging
from tenacity import (
    after_log,
    before_log,
    retry,
    stop_after_attempt,
    wait_fixed,
)

from core.config import settings
from .model import Model
from .sessions import engine


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("database")

MAX_RETIRES = 3
WAIT_SECONDS = 5 * 60   # 5 minutes

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


@retry(
    stop=stop_after_attempt(MAX_RETIRES),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def db_init() -> None:
    Model.metadata.naming_convention = convention

    async with engine.begin() as conn:
        logger.info(
            "Connection to %s", settings.SQLALCHEMY_DATABASE_URI_HIDDEN_PWD
        )
        # Tables should be created with Alembic migrations
        # But if you don't want to use migrations, create
        # the tables un-commenting the next line
        # await conn.run_sync(Model.metadata.create_all)

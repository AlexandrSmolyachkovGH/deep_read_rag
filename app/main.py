"""Main application file."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.connections.pg_conn import create_pg_handler
from app.core.temp_file_handler.dir_creation import TempDirHandler
from app.routers.users import user_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """App lifespan."""
    pg_handler = create_pg_handler()
    _app.state.pg = pg_handler

    tmp_handler = TempDirHandler()
    tmp_dir_path = await tmp_handler.create_tmp_file_dir()

    _app.state.tmp_dir = tmp_dir_path
    _app.state.tmp_handler = tmp_handler

    yield

    await pg_handler.dispose()
    await tmp_handler.remove_tmp_file_dir()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)

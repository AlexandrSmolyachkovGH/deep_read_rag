"""Create dir for temp files."""

import asyncio
import shutil
from collections.abc import Generator
from pathlib import Path

from fastapi import Request


class TempDirHandler:
    """Manage temp directory utility."""

    def __init__(self) -> None:
        """TempDirHandler init."""
        self.tmp_dir: Path | None = None

    async def create_tmp_file_dir(self) -> str:
        """Create dir for temp files."""
        project_dir = Path(__file__).parents[3]
        temp_file_dir_name = "temp_file_dir"

        temp_file_dir = project_dir / temp_file_dir_name

        await asyncio.to_thread(
            temp_file_dir.mkdir,
            exist_ok=True,
        )

        self.tmp_dir = temp_file_dir

        return str(temp_file_dir)

    async def remove_tmp_file_dir(self) -> None:
        """Remove temp dir."""
        if self.tmp_dir is None:
            return

        if await asyncio.to_thread(self.tmp_dir.exists):
            await asyncio.to_thread(
                shutil.rmtree,
                self.tmp_dir,
                True,
            )
            self.tmp_dir = None


def get_tmp_dir_path(
    request: Request,
) -> Generator[Path, None, None]:
    """Retrieve temp dir from request."""
    yield request.app.state.tmp_handler.tmp_dir

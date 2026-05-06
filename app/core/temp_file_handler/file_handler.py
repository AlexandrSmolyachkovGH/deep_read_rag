"""Temp file handler."""

import asyncio
from pathlib import Path

import aiofiles  # type: ignore[import-untyped]
from fastapi import UploadFile


class FileHandler:
    """Temp file handler."""

    async def create_temp_file(
        self,
        file: UploadFile,
        file_dir: Path,
    ) -> Path:
        """
        Save UploadFile to a temporary file.
        Return its path.
        """
        path = file_dir / file.filename
        async with aiofiles.open(
            file=path,
            mode="wb",
        ) as tmp_file:
            while chunk := await file.read(1024 * 1024):
                await tmp_file.write(chunk)

        return path

    async def delete_temp_file(
        self,
        file_path: Path,
    ) -> None:
        """Delete temp file."""
        await asyncio.to_thread(
            file_path.unlink,
            missing_ok=True,
        )


file_handler = FileHandler()

from fastapi import UploadFile
from aiofiles.os import remove
from uuid import uuid4
import asyncio
from app.model import File
import pandas as pd


class CsvUploader:
    def __init__(self) -> None:
        self.paths = []

    async def delete(self):
        await asyncio.gather(*(remove(path) for path in self.paths))

    def save(self, file: UploadFile, file_model: File):
            csv_name = uuid4()
            df = pd.read_csv(file.file)

            file_model.id = csv_name
            file_model.file_info={"columns": tuple(df.columns)}

            file.file.close()
            path = f"app/csv_storage/{csv_name}.{file.filename.rsplit('.')[-1]}"
            df.to_csv(path, index=False)
            self.paths.append(path)


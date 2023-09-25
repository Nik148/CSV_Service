from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import JSONResponse
from uuid import uuid4
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from aiofiles.os import remove
from collections import deque
import dask.dataframe as dd
import pandas as pd
import re

from .schema import FileDeleteSchema, QueryCsv, MyFileSchema
from .utils.queryCsvBuilder import QueryCsvBuilder
from .utils.csvUploader import CsvUploader
from .doc import load_csv_description, delete_csv_description, my_csv_description, query_csv_description
from app.auth import JWTBearer
from app.model import get_session, File


router = APIRouter(prefix="", tags=["CSV"])

@router.post("/csv", description=load_csv_description)
async def load_csv(file: UploadFile, 
                   token = Depends(JWTBearer()), 
                   session: AsyncSession = Depends(get_session)):
    if file.content_type != "text/csv":
        return JSONResponse(status_code=400, content={"message": "It is wrong content type"})
    csvUploader = CsvUploader()
    try:
        file_model = File(user_id=token["user_id"],
                        name=file.filename,
                        )
        csvUploader.save(file, file_model)
        session.add(file_model)
        await session.commit()
        return {"message": "Success"}
    except IntegrityError:
        await csvUploader.delete()
        await session.rollback()
        return JSONResponse(status_code=400,
                            content={"message": "This filename is used. Please rename file"})

@router.delete("/csv", description=delete_csv_description)
async def delete_csv(data: FileDeleteSchema, 
                    token = Depends(JWTBearer()),
                    session: AsyncSession = Depends(get_session)):
    file = await session.execute(select(File)
                           .where(File.user_id==token["user_id"])
                           .where(File.name==data.name)
                           )
    file: File = file.scalar()

    if not file:
        return JSONResponse(status_code=404, content={"message": "File not find"})
    
    id = file.id
    await session.delete(file)
    await session.commit()
    await remove(f"app/csv_storage/{id}.csv")
    return {"message": "Success"}

@router.get("/my_csv", response_model=List[MyFileSchema], description=my_csv_description)
async def get_my_csv(token = Depends(JWTBearer()), session: AsyncSession = Depends(get_session)):
    files = await session.execute(select(File)
                                  .where(File.user_id==token["user_id"]))
    files: List[File] = files.scalars().all()
    return files

@router.post("/query_csv/{filename}", description=query_csv_description)
async def query_csv(filename: str,
                    data: QueryCsv,
                    token = Depends(JWTBearer()),
                    session: AsyncSession = Depends(get_session)):
    file = await session.execute(select(File)
                           .where(File.user_id==token["user_id"])
                           .where(File.name==filename)
                           )
    file: File = file.scalar()

    if not file:
        return JSONResponse(status_code=404, content={"message": "File not find"})
    
    df = dd.read_csv(f'app/csv_storage/{file.id}.csv')
    query = QueryCsvBuilder(df, data)
    res = query.handleQuery()
    return JSONResponse(status_code=200, content=res)
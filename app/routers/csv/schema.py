from pydantic import BaseModel, Field
from typing import List, Union, Optional, Dict
    
    
class FileDeleteSchema(BaseModel):
    name: str

class MyFileSchema(BaseModel):
    name: str
    file_info: dict

    class Config:
        orm_mode = True

class QueryCsvFilter(BaseModel):
    column_name: str
    filter: str
    value: Union[int, str]

class QueryCsvSorted(BaseModel):
    column_name: str
    sort: str

class QueryCsv(BaseModel):
    column: List[str]
    filters: Dict
    sorted: Optional[List[QueryCsvSorted]] = Field(default=[])

    class Config:
        schema_extra = { "example": {
                        "column": [
                            "string"
                        ],
                        "filters": {
                            "or":
                                [
                                    {"compare": {
                                    "column_name": "age",
                                    "filter": "GREATER_THAN",
                                    "value": 0
                                    }},
                                    {"compare": {
                                    "column_name": "name",
                                    "filter": "EQUALS",
                                    "value": "Nik"
                                    }}
                                ]
                        },
                        "sorted": [
                            {
                            "column_name": "string",
                            "sort": "string"
                            }
                        ]
                        }}
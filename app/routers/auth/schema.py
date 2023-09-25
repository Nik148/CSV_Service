from pydantic import BaseModel, root_validator
from app.dependencies import password_context

class UserLoginSchema(BaseModel):
    login: str
    password: str

class UserRegisterSchema(UserLoginSchema):
        
    class Config:
        orm_mode = True

    @root_validator()
    def formatedField(cls, v):
        v["password"] = password_context.hash(v["password"])
        return v
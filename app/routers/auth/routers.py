from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .schema import UserLoginSchema, UserRegisterSchema
from .doc import login_description, registration_description
from app.model import get_session, User
from app.dependencies import password_context
from app.auth import signJWT


router = APIRouter(prefix="", tags=["Auth"])

@router.post("/registration", description=registration_description)
async def registration(data: UserRegisterSchema, session: AsyncSession = Depends(get_session)):
    user = User(data)
    session.add(user)
    try:
        await session.commit()
        return {"message": "Success"}
    except IntegrityError:
        return JSONResponse(status_code=400, content={"message": "login is busy"}) 

@router.post("/login", description=login_description)
async def login(data: UserLoginSchema, session: AsyncSession = Depends(get_session)):
    user = await session.execute(select(User).where(User.login==data.login))
    user: User = user.scalar() 
    if user and password_context.verify(data.password, user.password):
        return signJWT(user.id)
    return JSONResponse(status_code=400, content={"message": "Not login"}) 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Integer, String, Column, UUID, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from config import Config
from app.routers.auth.schema import UserRegisterSchema


Base = declarative_base()
engine = create_async_engine(Config.DB_URL)
async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(), index=True, unique=True, nullable=False)
    password = Column(String(), nullable=False)

    files = relationship(
        "File", back_populates="user", lazy="select", cascade="all,delete"
    )

    def __init__(self, dataObj: UserRegisterSchema):
        self.__dict__.update(dataObj.dict())

class File(Base):
    __tablename__ = "file"
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(), nullable=False)
    file_info = Column(JSONB, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship(
        "User", back_populates="files", lazy="select"
    )

    __table_args__ = (UniqueConstraint('user_id', 'name'),
                     )

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from enum import Enum
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/main",
    tags=["main"],
    dependencies=[Depends(auth.get_api_key)],
)
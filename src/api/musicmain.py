from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from enum import Enum
import sqlalchemy
from src import database as db
from typing import Dict

@router.get("/musicmain/", tags=["musicmain"])
def search_characters(
        character_name: str = "",
        sort_col: str = "",
        sort_order: str = "",
    ):

    print("on")
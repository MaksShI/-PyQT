from typing import List

from fastapi import APIRouter, Depends, HTTPException
from server import User
from api import deps
from api import crud
from api import schemas
from sqlalchemy.orm import Session

router = APIRouter


@router.get("/", response_model=List[schemas.User])
async def read_user(db: Session = Depends(deps.get_db)):
    data = crud.get_multi(db=db, server=User)
    return data


@router.post("/", response_model=schemas.User)
def create_user(user_in: schemas.UserBase, db: Session = Depends(deps.get_db)):
    user = crud.get_by_login(db=db, server=User, login=user_in.login)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this phone number already exists in the system.",
        )
    user = crud.create(db=db, obj_in=user_in)
    return user

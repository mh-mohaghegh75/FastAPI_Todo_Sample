import sys
from typing import Optional
from fastapi import Depends, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

import model
from database import SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from routers.auth import get_current_user

sys.path.append("..")

router = APIRouter(prefix="/address", tags=["address"], responses={404: {"description": "Not Found"}})


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Address(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    stats: str
    country: str
    postalcode: str


@router.post("/")
async def create_address(address: Address,
                         user: dict = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail=jsonable_encoder({"Message": "User Not Found"}))
    address_model = model.Address()
    address_model.address1 = address.address1
    address_model.address2 = address.address2
    address_model.city = address.city
    address_model.state = address.state
    address_model.country = address.country
    address_model.postalcode = address.postalcode

    db.add(address_model)
    db.flush()

    user_model = db.query(model.Users).filter(model.Users.id == user.get("id")).first()

    user_model.address_id = address_model.id

    db.add(user_model)
    db.commit()

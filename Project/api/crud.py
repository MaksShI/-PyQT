from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session


def get_by_id(db: Session, server, id: int):
    return db.query(server).filter(server.id == id).first


def get_by_login(db: Session, server, login: str):
    return db.query(server).filter(server.login == login).first


def get_multi(db: Session, server):
    objects = db.query(server)
    return objects.all()


def create(db: Session, server, obj_in):
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = server(**obj_in_data)
    db.add(db_obj)
    db.commit()
    return db_obj

from app.db.session import SessionLocal
from app.db.init_db import init_db


def init():
    db = SessionLocal()
    init_db(db)


def pre_start():
    init()

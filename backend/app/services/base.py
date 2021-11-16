from typing import TypeVar, Dict, Any, Union, Generic, Type, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model

    def get(self, model_id: int) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == model_id).first()

    def get_list(self, skip: int = 0, limit: int = 100):
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def commit(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_update_data(self, update: Union[UpdateSchemaType, Dict[str, Any]]):
        if isinstance(update, dict):
            update_data = update
        else:
            update_data = update.dict(exclude_unset=True)
        return update_data

    def create(self, create: CreateSchemaType) -> ModelType:
        create_data = jsonable_encoder(create)
        obj = self.model(**create_data)
        return self.commit(obj)

    def update(
        self,
        obj: ModelType,
        update: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(obj)
        update_data = self.get_update_data(update)
        for field in obj_data:
            if field in update_data:
                setattr(obj, field, update_data[field])

        return self.commit(obj)

    def remove(self, model_id: int) -> ModelType:
        obj = self.db.query(self.model).get(model_id)
        self.db.delete(obj)
        self.db.commit()
        return obj

from app.models.mongo.model import MongoModel
from app.schemas.money.tag import Tag
from app.core.config import MONGO_MONEY_DB

Tag = MongoModel(MONGO_MONEY_DB, 'Tag', Tag)
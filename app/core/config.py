from app.core.constants import ENV
from app.db.mongo import Mongo

MONGO_CLIENT = Mongo().connect()
MONGO_MONEY_DB = MONGO_CLIENT['test_money'] if ENV == 'TEST' else MONGO_CLIENT['money'] 


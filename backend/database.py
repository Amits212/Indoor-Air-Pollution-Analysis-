
from motor.motor_asyncio import AsyncIOMotorClient



client = AsyncIOMotorClient('mongodb://mongo:27017')
db = client.db
buildings_collection = db.buildings

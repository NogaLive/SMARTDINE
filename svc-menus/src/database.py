import os
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis

# Configuración de conexión (Variables de entorno o defaults)
MONGO_URL = os.getenv("MONGO_URL", "mongodb://admin:password@localhost:27017")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

class Database:
    client: AsyncIOMotorClient = None
    redis_client: redis.Redis = None

    def connect(self):
        self.client = AsyncIOMotorClient(MONGO_URL)
        self.redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        print("Conectado a MongoDB y Redis")

    def close(self):
        self.client.close()
        self.redis_client.close()

db = Database()
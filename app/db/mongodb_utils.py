import logging

from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT
from .mongodb import db


async def connect_to_mongo():
    logging.info("Conectando-se ao banco de dados...")
    db.client = AsyncIOMotorClient(
        str(MONGODB_URL),
        maxPoolSize=MAX_CONNECTIONS_COUNT,
        minPoolSize=MIN_CONNECTIONS_COUNT
    )
    logging.info("Foi conectado com sucesso ao banco de dados")


async def close_mongo_connection():
    logging.info("fechando a conexao ao banco de dados...")
    db.client.close()
    logging.info("Conexao com o banco de dados fechada")

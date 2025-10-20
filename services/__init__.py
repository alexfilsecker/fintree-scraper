from config import envs
from .mongo import MongoService

mongo_service = MongoService(envs.MONGO_CONNECTION_STRING, envs.MONGO_DB)


if __name__ == "__main__":
    mongo_service.upload_document("hola", {"peo", "caca"})
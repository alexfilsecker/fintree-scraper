import os
from dotenv import load_dotenv

class Environments:
    MONGO_CONNECTION_STRING: str
    MONGO_DB: str

    def __init__(self):
        load_dotenv()
        for key in self.__annotations__:
            value = os.getenv(key)
            if not value:
                raise KeyError(f"key {key} not present in environment variables")
            
            setattr(self, key, value)


if __name__ == "__main__":
    envs = Environments()
    print(envs.MONGO_CONNECTION_STRING)



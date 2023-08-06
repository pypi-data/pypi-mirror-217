import abc
from dddmisc import AbstractAsyncRepository
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorCollection
from typing import Mapping


class AbstractMongoRepository(AbstractAsyncRepository, abc.ABC):

    def __init__(self, connection: AsyncIOMotorClientSession, collections: Mapping[str, AsyncIOMotorCollection]):
        super().__init__(connection)
        self._collections = collections

    def _get_mongo_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        return self._collections[collection_name]

from bson import UuidRepresentation, CodecOptions
from dddmisc import AbstractAsyncUnitOfWork
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorClientSession
from types import MappingProxyType
from typing import Iterable, Mapping
from functools import partial

from .abstraction import AbstractMongoRepository


class MongoEngine:
    def __init__(
            self,
            address: str,
            db_name: str,
            collections: Iterable[str],
            codec_options: CodecOptions = None,
    ):
        self._client = AsyncIOMotorClient(address)
        self._db = self._client[db_name]
        collections_with_options = self._get_collections_with_options(collections, codec_options)
        self._collections = MappingProxyType(collections_with_options)

    def get_collections(self) -> Mapping[str, AsyncIOMotorCollection]:
        return self._collections

    async def get_session(self) -> AsyncIOMotorClientSession:
        return await self._client.start_session()

    def _get_collections_with_options(self, collections: Iterable[str], codec_options: CodecOptions):
        collections_with_options = dict()
        codec_options = codec_options or CodecOptions(
            tz_aware=True,
            uuid_representation=UuidRepresentation.STANDARD
        )
        for collection in collections:
            collections_with_options[collection] = self._db[collection].with_options(codec_options)
        return collections_with_options


class MongoMotorUOW(AbstractAsyncUnitOfWork):

    def __init__(self, engine: MongoEngine, repository_class: AbstractMongoRepository):
        if not issubclass(repository_class, AbstractMongoRepository):
            raise TypeError('Repository class in "MongoMotorUOW" must be subclass of "AbstractMongoRepository"')
        repository_class = partial(repository_class, collections=engine.get_collections())
        super().__init__(engine, repository_class)

    async def _begin_transaction(self, mongo_engine: MongoEngine) -> AsyncIOMotorClientSession:
        self._mongo_session = await mongo_engine.get_session()
        session_context = await self._mongo_session.__aenter__()
        self._trn_context = session_context.start_transaction()
        await self._trn_context.__aenter__()
        return session_context

    async def _commit_transaction(self, session_context) -> None:
        if hasattr(self, '_trn_context'):
            await session_context.commit_transaction()
            await self._trn_context.__aexit__(None, None, None)
            delattr(self, '_trn_context')
            await self._mongo_session.__aexit__(None, None, None)
            delattr(self, '_mongo_session')
        else:
            raise RuntimeError('Database transaction not found')

    async def _rollback_transaction(self, session_context) -> None:
        if hasattr(self, '_trn_context'):
            await session_context.abort_transaction()
            trn_context = self._trn_context
            await trn_context.__aexit__(None, None, None)
            delattr(self, '_trn_context')
            await self._mongo_session.__aexit__(None, None, None)
            delattr(self, '_mongo_session')

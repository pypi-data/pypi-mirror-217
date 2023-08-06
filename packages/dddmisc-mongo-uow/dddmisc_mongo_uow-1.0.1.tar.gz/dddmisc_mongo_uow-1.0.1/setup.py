# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dddmisc_mongo_uow']

package_data = \
{'': ['*']}

install_requires = \
['ddd-misc>=0.8.1,<0.9.0', 'motor>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'dddmisc-mongo-uow',
    'version': '1.0.1',
    'description': '',
    'long_description': '# MongoDB async ddd-misc UnitOfWork\n\nMongoDB UnitOfWork на базе ddd-misc и библиотеки Motor: Asynchronous Python driver for MongoDB.\n\n\n## Классы\n\n**AbstractMongoRepository**\n\nAbstractMongoRepository - абстрактный класс для реализации репозитория с подключением к базе данных MongoDB. Класс реализует \nсигнатуру для инициализации с двумя параметрами помимо self и метод \'get_mongo_collection\':\n\n    - \'connection\' - параметр принимающий контекст инстанса класса AsyncIOMotorClientSession библиотеки Motor.\n\n    - \'collections\' - параметр принимающий структуру dict ключами которой являются название mongo коллекции в виде строки, а значениями объект класса AsyncIOMotorCollection библиотеки Motor.\n\n    \'_get_mongo_collection\' - метод класса AbstractMongoRepository, возвращающий mongo коллекцию по передаваемому названию в параметре в виде строки.\n\nДанный класс обязателен для наследования при реализации конкретного MongoDB репозитория в рамках UnitOfWork данного пакета.\n\nПример использования:\n```\nfrom dddmisc_mongo_uow import AbstractMongoRepository\n\n\nclass ConcreteMongoRepository(AbstractMongoRepository):\n    aggregate_class = ConcreteAggregateClass\n    \n    async def _add_to_storage(self, aggregate):\n        document = dict(\n            key=aggregate._key,\n            reference=str(aggregate.reference)\n        )\n        collection = self._get_mongo_collection(\'uow\')\n        await collection.update_one({\'reference\': document[\'reference\']}, {\'$set\' : document}, upsert=True, session=self._connection)\n```\n\n**MongoEngine**\n\nMongoEngine - класс для создания структуры engine MongoDB версии, engine передается в параметры при инициализации AsyncMessageBus.\nПри инициализации MongoEngine требует трех обязательных параметров:\n\n    - \'address\' - параметр принимающий строку для подключения к конкретной базе данных MongoDB, включающей в себя хост базы, а так же дополнительные параметры подключения. Пример - \'mongodb://localhost:27017/?directConnection=true\'. При инициализации по параметру создается объект AsyncIOMotorClient.\n\n    - \'db_name\' - параметр принимающий строку с названием базы данных. При инициализации создается объект AsyncIOMotorDatabase.\n\n    - \'collections\' - парамтер принимающий массив с названиями коллекции MongoDB в виде строк. При инициализации создается структура неизменяемого dict, ключами которой являются названия коллекции, а значениями объекты AsyncIOMotorCollection с подключением к данным коллекциям.\n\n    \'get_collections\' - метод возвращающий коллекции.\n\n    \'get_session\' - асинхронный метод возврщающий объект AsyncIOMotorClientSession для проведения транзакции.\n\nПример использования:\n```\nfrom dddmisc_mongo_uow import MongoEngine\n\n\nmongo_engine = MongoEngine(address=\'mongodb://localhost:27017/?directConnection=true\', db_name=\'mongo_uow\', collections=[\'uow\'])\n\ncollections = mongo_engine.get_collections()\n\nsession = await mongo_engine.get_session()\n```\n\n**MongoMotorUOW**\n\nMongoMotorUOW - класс на базе AbstractAsyncUnitOfWork, реализующий конкретный объект UnitOfWork и его стандартное поведение в рамках ddd-misc для выполнения транзакции в MongoDB.\n\nКласс реализует стандартную сигнатуру для создания объекта UnitOfWork в процессе выполнения хэндлера в объекте AsyncMessageBus, требующую двух параметров engine и repository_class. В процессе инициализации проверяется является ли repository_class субклассом AbstractMongoRepository, далее repository_class оборачивается классом декоратором вместе с параметром collections, чтобы UnitOfWork мог передавать один параметр connection при инициализации репозитория.\n\nПример использования:\n```\nfrom dddmisc import AsyncMessageBus\nfrom dddmisc_mongo_uow import MongoMotorUOW\n\nmessage_bus = AsyncMessageBus(\n    uow_class=MongoMotorUOW,\n    repository_class=ConcreteMongoRepository,\n    engine=mongo_engine\n)\n```\n\n\n## Основные параметры для запуска MongoDB в .gitlab-ci.yml:\n```\n  services:\n    - name: mongo:6.0\n      alias: mongo-svc\n      command: ["mongod", "--logpath=/dev/null", "--bind_ip_all", "--replSet=rs0"]\n  before_script:\n    - python -V\n    - python -m venv .venv\n    - poetry install\n    - apt-get update && apt-get install -y gnupg\n    - apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*\n    - wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -\n    - echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/6.0 main" |  tee /etc/apt/sources.list.d/mongodb-org-6.0.list\n    - apt-get update\n    - apt-get install -y mongodb-org\n    - mongosh --host mongo-svc --eval "rs.initiate({\'_id\':\'rs0\',\'members\':[{\'_id\':0,\'host\':\'127.0.0.1:27017\'}]});"\n  script:\n    - mongosh --host mongo-svc --eval "rs.status()"\n    - poetry run poe test\n```\n\nПри установке отличающейся версии MongoDB параметры установки нужно изменить на акутальную версию.\n\nКомманда `rs.initiate({\'_id\':\'rs0\',\'members\':[{\'_id\':0,\'host\':\'mongo-svc\'}]});` инициирует реплику.\n\n\nНа странице https://www.mongodb.com/docs/manual/reference/connection-string/ описан формат строки подключения и разные его варианты.\n\n\nСтандартный формат подключения:\n\n    - \'mongodb://localhost:27017/\'\n\nРабочий формат подключения на локальном компьютере при инициации \'rs.initiate()\':\n\n    - \'mongodb://localhost:27017/?directConnection=true\'\n\nПри инициации \'rs.initiate({\'_id\':\'rs0\',\'members\':[{\'_id\':0,\'host\':\'mongo-svc\'}]})\' создается конкретная реплика, их может быть несколько, например:\n\n```\n    rs.initiate(\n    {\n        _id: "rs0",\n        version: 1,\n        members: [\n            { _id: 0, host : "mongodb0.example.net:27017" },\n            { _id: 1, host : "mongodb1.example.net:27017" },\n            { _id: 2, host : "mongodb2.example.net:27017" }\n        ]\n    }\n    )\n```\n\'rs0\' - имя набора реплик, задается при поднятии базы, строка подключения на локалке:\n\n    - \'mongodb://localhost:27017/?directConnection=true&replicaSet=rs0',
    'author': 'Aziz',
    'author_email': 'walkingonadream2012@mail.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

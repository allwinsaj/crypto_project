from oslo_config import cfg


class DatabaseAdapter(object):
    def __init__(self,
                 /,
                 collection_name="test") -> None:
        self.__host = cfg.CONF.database.host
        self.__port = cfg.CONF.database.port
        self.__username = cfg.CONF.database.username
        self.__password = cfg.CONF.database.password
        self.__auth_database = cfg.CONF.database.database
        self.__database_name = cfg.CONF.database.name
        self.__collection_name = cfg.CONF.database.collection_name
        self.__client = self.connect_database()

    def set_collection_name(self, collection_name):
        self.__collection_name = collection_name

    def connect_database(self):
        try:
            # if self.__username and self.__password and self.__auth_database:
            #     uri = f"mongodb://{self.__username}:{self.__password}@mongodb:{self.__port}/{self.__auth_database}"
            # else:
            uri = f"mongodb://mongodb:{self.__port}"
            from pymongo import MongoClient
            client = MongoClient(uri)
            return client.get_database(self.__database_name)
        except:
            raise

    def connect_collection(self):
        db = self.__client
        # Check if the collection exists
        if self.__collection_name not in db.list_collection_names():
            # Create the collection if it does not exist
            db.create_collection(self.__collection_name)

        # Return the collection object
        coll = db[self.__collection_name]
        return coll

    def find_document(self,
                      query):
        conn = self.connect_collection()
        result = conn.find_one(query)
        return result

    def find_documents(self,
                       query,
                       /,
                       *,
                       exclude_fields: list[str] = None,
                       include_fields: list[str] = None,
                       skip_val=0,
                       limit=0):
        query_fields = {}
        if exclude_fields:
            query_fields.update(dict((field, 0) for field in exclude_fields))
        if include_fields:
            query_fields.update(dict((field, 1) for field in include_fields))
        conn = self.connect_collection()
        result = conn.find(query,
                           projection=query_fields)
        if limit:
            result = result.skip(skip_val).limit(limit)
        return result

    def get_count(self,
                  query):
        conn = self.connect_collection()
        return conn.count_documents(query)

    def get_distinct(self,
                     field_name,
                     query):
        conn = self.connect_collection()
        return conn.distinct(field_name,
                             filter=query)

    def insert_documents(self,
                         documents: list[dict]):
        conn = self.connect_collection()
        result = conn.insert_many(documents,
                                  ordered=False)
        return result

    def insert_document(self,
                        document: dict):
        conn = self.connect_collection()
        result = conn.insert_one(document)
        return result

    def update_document(self,
                        query,
                        updated_document,
                        upsert):
        conn = self.connect_collection()
        result = conn.update_one(query, updated_document,
                                 upsert=upsert)
        return result

from pymongo import MongoClient

class Mongo:

    def __init__(self, host='localhost', port=27017):
        self.client = MongoClient(host, port)

    def get_db(self, db_name):
        return self.client[db_name]
    
    def get_collection(self, db, colle_name):
        return db[colle_name]

    def insert_doc(self, db, doc_name, doc):
        docs = self.get_collection(db, doc_name)
        return docs.insert(doc)

    def bulk_insert(self, db, doc_name, new_docs):
        docs = self.get_collection(db, doc_name)
        return docs.insert(new_docs)

import pymongo

class DB():
    uri         = 'localhost'
    port        = 27017
    client      = None
    db_name     = None
    curr_db     = None

    def __init__(self, uri:str='localhost', port:int=27017, db_name:str=''):
        self.uri = uri
        self.port = port
        self.db_name = db_name
        self.client = self.conn(self.uri, self.port)
        self.curr_db = self.set_db(db_name)
        
    def conn(self, uri:str='', port:int=0) -> pymongo.MongoClient:
        return pymongo.MongoClient(uri, port)
    
    def set_db(self, db_name:str='') -> pymongo.database.Database:
        return self.client[db_name]

    def get_database_list(self) -> list:
        return self.client.list_database_names()
    
    def get_collection_list(self) -> list:
        return self.curr_db.list_collection_names()
    
    def get_item_from(self, collection:str='', query:dict={}) -> dict:
        return self.curr_db[collection].find_one(query)
    
    def get_all_from(self, collection:str='', query:dict={}, filter:dict={}, sort:str='', accending:bool=True) -> list:
        return self.curr_db[collection].find(query).sort(sort, 1 if accending else -1)

## testing and debugging some stuff
if __name__ == '__main__':
    db = DB('localhost', 27017, 'rpg-tables')
    #print(db.get_database_list())
    #print(db.get_collection_list())
    item = 'bag of hold'
    res = db.get_item_from('items-5e', {"Name": {'$regex': f'{(item).replace("+", "[+]")}', "$options": "i"}})
    if res == None:
        print("Nothing Found")
    else:
        print(type(res))

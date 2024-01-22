from .db_config import client

"""Aggregation query on database"""


async def db_aggregation(db_name: str, collection_name: str, pipeline):
    # Defining db and collection name
    db = client[f"{db_name}"]
    collection = db[f"{collection_name}"]

    # Fetch the aggregated result
    results = collection.aggregate(pipeline=pipeline)

    return list(results)


"""Find one query on database"""


async def db_find_one(db_name: str, collection_name: str, filter: dict):
    # Defining db and collection name
    db = client[f"{db_name}"]
    collection = db[f"{collection_name}"]

    # Execute the find query on db
    result = collection.find_one(filter)

    return result


"""Query to insert one data"""


async def db_insert_one(db_name: str, collection_name: str, data: dict):
    # Defining db and collection name
    db = client[f"{db_name}"]
    collection = db[f"{collection_name}"]

    # Execute the insert query
    collection.insert_one(data)


"""Query to fetch all records from a collection"""


async def db_fetch_all(db_name: str, collection_name: str):
    # Defining db and collection name
    db = client[f"{db_name}"]
    collection = db[f"{collection_name}"]

    # Execute the query
    result = collection.find()

    return result


"""Query to delete data from a collection"""


async def db_delete(db_name: str, collection_name: str, filter: dict):
    # Defining db and collection name
    db = client[f"{db_name}"]
    collection = db[f"{collection_name}"]

    # Execute the delete query
    collection.delete_one(filter)

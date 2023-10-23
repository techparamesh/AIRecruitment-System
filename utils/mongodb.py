from pymongo import MongoClient

mongodb_connection = MongoClient('mongodb+srv://perfectpatterns2023:perfectpatterns2023@cluster0.u0etc20.mongodb.net/?retryWrites=true&w=majority')
db = mongodb_connection["CandidatesDatadb"]


# Function to create new collection in our CandidatesData database
def collection_creation(collection_name: str):
    new_collection = db[collection_name]
    return new_collection


# Function to insert list of JSON records into a specified collection
def records_insertion(records: list, collection):
    try:
        i = collection.insert_many(records, ordered = False)
        print(len(i.inserted_ids), "Records inserted successfully!")
    except:
        print('Duplicate records found')


# Function to return records from the specified collection matching the query parameter
def fetch_records(collection, query = None):
    return collection.find(query)


# Function to return count of records from the specified collection matching the query parameter
def count_records(collection, query = {}):
    return collection.count_documents(query)


# Function to delete records in a specified collection
def records_deletion(query, collection):
    d = collection.delete_many(query)
    print(d.deleted_count, "Records deleted successfully!")
    

# Function to update a record in a specified collection by its ID
def record_updation(id: int, update_query: dict, collection):
    collection.find_one_and_update({"_id": id}, update_query, upsert = False)
    print("1 record updated successfully!")
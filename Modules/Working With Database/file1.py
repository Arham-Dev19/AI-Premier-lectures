from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["new"]
collection = db["table"]

print("MongoDB Connected Succesfully")

# Cruds # Create, Update, Delete

# Insert One
table = {
    "name": "Ali",
    "age": 21,
    "course": "Pyhton"
}

collection.insert_one(table)
print("Data Inserted")


# Insert Many
table = [
    {"name":"Asif", "age":33},
    {"name":"Aleena", "age":24}
]

collection.insert_many(table)


# fetch data
for data in collection.find():
    print(table)
from pymongo import MongoClient
from pymongo import DESCENDING
from datetime import datetime
from bson.objectid import ObjectId
from kbsbot.channel_handler.services import *

client = MongoClient("mongodb://localhost:27017/")
db = client["interactions_db"]
interactions = db["interactions"]


def get_all_user_inputs(user_id):
    inter = interactions.find({"user": user_id})
    # print(inter)
    for aux in inter:
        print(aux)


def create_entry(user, entry):
    today = datetime.now()
    new_entry = {
        "user": user.id,
        "social_network": user.channel_id,
        "input": entry
    }
    # print("NEW", new_entry)
    try:
        last_parent_interaction = \
            interactions.find({"user": user.id, "social_network": user.channel_id, "parent": None},
                              sort=[('_id', DESCENDING)])[0]
        superior_interactions = interactions.find(
            {"user": user.id, "social_network": user.channel_id,
             "date": {"$gte": last_parent_interaction["date"]}}, sort=[('_id', DESCENDING)])
        last_interaction = superior_interactions[0]
        # print("LAST", last_interaction)
        if last_interaction["date"].date() == today.date():
            # Checking if time between interactions is less than 15 minutes
            if today.timestamp() - last_interaction["date"].timestamp() <= 900:
                new_entry["parent"] = last_interaction["_id"]
            else:
                new_entry["parent"] = None
    except IndexError:
        print("No records found")
        new_entry["parent"] = None
    finally:
        new_entry["date"] = today
        # print("NEW FINAL", new_entry)
        new_interaction = interactions.insert_one(new_entry)
        replicate_entry(user, new_entry, "POST")
        return new_interaction.inserted_id


def update_entry(entry_id, output):
    interactions.update_one({'_id': ObjectId(entry_id)}, {'$push': {"output": output}})
    # TODO replicate entry
    # replicate_entry(user, entry, "PUT")


def find_in_context(user, entities=["http://127.0.0.1/ockb/resources/Course"]):
    try:
        last_parent_interaction = \
            interactions.find({"user": user.id, "social_network": user.channel_id, "parent": None},
                              sort=[('_id', DESCENDING)])[0]
        superior_interactions = interactions.find(
            {"user": user.id, "social_network": user.channel_id,
             "date": {"$gte": last_parent_interaction["date"]}}, sort=[('_id', DESCENDING)])
        last_interaction = superior_interactions[0]
        # print("LAST", last_interaction)
        for las in superior_interactions:
            print("sup", las)
    except IndexError:
        print("No records found")

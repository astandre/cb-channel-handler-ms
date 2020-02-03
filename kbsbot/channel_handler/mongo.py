from pymongo import MongoClient
from pymongo import DESCENDING, ASCENDING
from datetime import datetime
from bson.objectid import ObjectId
import os

MONGO_HOST = os.environ.get('MONGO_HOST')
client = MongoClient(MONGO_HOST)

# client = MongoClient("mongodb://localhost:27017/")
db = client["interactions_db"]
interactions = db["interactions"]


def get_all_user_inputs(user_id):
    inter = interactions.find({"user": user_id})
    # print(inter)
    for aux in inter:
        print(aux)


def create_entry(user, entry):
    """
    This method creates an entry in the conversation thread between the user and the chatbot.
    The id of the current channel is also stored.

    Parameters:
        :param user: The user object containing all the information of the user.

        :param entry: The current entry of the conversation, the input context is also stored.

    Return:
        The id of the current interaction stored.

      """
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
        return new_interaction.inserted_id


def update_entry(entry_id, output):
    """
    This method updates the output of the current conversation thread.

     Parameters:

        :param entry_id: The id of the message.

        :param output: The output context of the interaction.
    """
    interactions.update({'_id': ObjectId(entry_id)}, {'$set': {"output": output}})


def get_last_thread(user):
    """
     Parameters:

        :param user: The user object containing all the information of the user.

    """
    last_interactions_list = []
    try:
        last_parent_interaction = \
            interactions.find({"user": user.id, "social_network": user.channel_id, "parent": None},
                              sort=[('_id', DESCENDING)])[0]
        superior_interactions = interactions.find(
            {"user": user.id, "social_network": user.channel_id,
             "date": {"$gte": last_parent_interaction["date"]}}, sort=[('_id', ASCENDING)])

        for inter in superior_interactions:
            del inter["_id"]
            if "parent" in inter:
                del inter["parent"]
            last_interactions_list.append(inter)
        return last_interactions_list
    except Exception as e:
        print("No records found", e)
        return last_interactions_list

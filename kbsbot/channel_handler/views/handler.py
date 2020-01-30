from flakon import JsonBlueprint
from flask import request
from kbsbot.channel_handler.mongo import *
from kbsbot.channel_handler.database import *
from kbsbot.channel_handler.services import *

handler = JsonBlueprint('handler', __name__)


@handler.route('/chat', methods=["POST"])
def chat():
    """
    This view is used by the channel to authenticate and communicate with the compose engine.
    In order to retrieve an answer for the user.
    This method requires a dict with the following information:

    Args:
        @param: token: Authentication token.

        @param: user: A dict containing the user_name, name, last_name and if exists social_network_id

        @param: input: A dict containing the input of the user: user_input (Raw input of the user), a context dict containing: An intent if exists and a list of entities if exists.
    """
    data = request.get_json()
    if "token" in data:
        channel = get_channel_id(data["token"])
        agent = channel.agent.name
        if channel is not None:
            user = get_or_create_user(data["user"], channel)

            entry = create_entry(user, data["input"])
            compose_data = {
                "agent": agent,
                "user": user.id,
                "channel": channel.id,
                "user_input": data["input"]["user_input"],
                "context": data["input"]["context"]

            }
            output = compose(compose_data)
            update_entry(entry, output)
            return output
        return {"message": "token is no correct", "status": False}
    else:
        return {"message": "token is no correct", "status": False}


@handler.route('/thread/last', methods=["GET"])
def user_last_thread():
    """
    This view returns a list of the last interactions of the user in a selected network.
    The list if ordered in an ascending way.
    Starting from the last parent interaction.

    Args:
        @param: user: This view requires an id of a user.

    """
    data = request.get_json()
    if "user" in data:
        user = get_user(data["user"])
        last_inter = get_last_thread(user)
        return {"interactions": last_inter, "user": user.id, "channel": user.channel.id,
                "agent": user.channel.agent.name}
    else:
        return {"message": "Must provide a valid user id"}

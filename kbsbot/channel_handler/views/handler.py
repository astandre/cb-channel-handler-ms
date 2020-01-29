from flakon import JsonBlueprint
from flask import request
from kbsbot.channel_handler.mongo import *
from kbsbot.channel_handler.database import *
from kbsbot.channel_handler.services import *

handler = JsonBlueprint('handler', __name__)


@handler.route('/chat', methods=["POST"])
def chat():
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
    data = request.get_json()
    user = get_user(data["user"])
    last_inter = get_last_thread(user)
    return {"interactions": last_inter, "user": user.id, "channel": user.channel.id, "agent": user.channel.agent.name}

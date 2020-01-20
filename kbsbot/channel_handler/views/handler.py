from flakon import JsonBlueprint
from flask import request
from kbsbot.channel_handler.mongo import *
from kbsbot.channel_handler.database import *

handler = JsonBlueprint('handler', __name__)


@handler.route('/chat', methods=["POST"])
def chat():
    data = request.get_json()
    if "token" in data:
        channel = get_channel_id(data["token"])
        agent = None
        if channel is not None:
            user = get_or_create_user_channel(data["user"], channel)

            entry = create_entry(user, data["input"])
            compose_data = {
                "agent": agent,
                "user": user.id,
                "channel": channel.id,
                "user_input": entry["input"]["user_input"],
                "context": entry["input"]["context"]

            }
            output = compose(compose_data)
            update_entry(entry, output)
            return output
        return {"message": "token is no correct", "status": False}
    else:
        return {"message": "token is no correct", "status": False}

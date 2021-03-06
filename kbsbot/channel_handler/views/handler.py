from flakon import JsonBlueprint
from flask import request
from kbsbot.channel_handler.mongo import *
from kbsbot.channel_handler.database import *
from kbsbot.channel_handler.services import *
import logging

handler = JsonBlueprint('handler', __name__)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


@handler.route('/status', methods=["GET"])
def get_status():
    return {"message": "ok"}


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
    logger.info(">>>>> Incoming data  %s", data)
    if "token" in data:
        channel = get_channel_id(data["token"])
        agent = channel.agent.name
        if channel is not None:
            user = get_or_create_user(data["user"], channel)
            if len(data["input"]) > 0:
                entry = create_entry(user, data["input"], agent)
            compose_data = {
                "agent": agent,
                "user": {"id": user.id},
                "channel": channel.id,
                "user_input": data["input"]["user_input"],
                "context": data["input"]["context"]
            }
            if "help" in data["input"] and data["input"]["help"] is True:
                compose_data["help"] = True
            output = compose(compose_data)
            if len(data["input"]) > 0:
                update_entry(entry, output)
            logger.info("<<<<< Output  %s", output)
            return output
        else:
            return {"message": "token is no correct", "status": False}
    else:
        return {"message": "token is no correct", "status": False}


@handler.route('/about/agent', methods=["GET"])
def get_about_agent():
    """
    This method returns general information of the agent, like the name and the about.

    Args:
        @param: token: Authentication token.
    """
    data = request.get_json()
    if "token" in data:
        channel = get_channel_id(data["token"])
        if channel is not None:
            agent = channel.agent
            return {"about": agent.about, "name": agent.name}
        else:
            return {"message": "token is no correct", "status": False}
    else:
        return {"message": "token is no correct", "status": False}

import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import EncryptedType
import os

db = SQLAlchemy()

key = os.environ.get('KEY')


# key = "9WhoO2zEai7PveqOKEbatLobHCj45FLci6rtROxqpE4="


class SocialNetwork(enum.Enum):
    twitter = 'twitter'
    telegram = 'telegram'
    other = 'other'


class Agent(db.Model):
    """Agent

    An Agent refers to the main o domain or purpose of the chatbot.

    Attributes:
        :param @id: Id to populate the database.

        :param @name: This name must be unique to identify the Agent.

        :param @about: A description of the purpose of the chatbot.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    about = db.Column(db.String(140), nullable=False)

    def __repr__(self):
        return f"<Agent {self.name}>"


class Channel(db.Model):
    """
    A communication channel used to interact with the user and the system.

    Attributes:
        :param @id: Id to populate the database.

        :param @name: The name or address of the channel

        :param @agent_id: The id of the agent containing this channel

        :param @agent: Tha object agent containing this channel

        :param @social_network: The name of the social network used
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    token = db.Column(EncryptedType(db.String, key), nullable=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'),
                         nullable=False)
    agent = db.relationship('Agent', backref=db.backref('channels', lazy=True))
    social_network = db.Column(
        db.Enum(SocialNetwork),
        default=SocialNetwork.telegram,
        nullable=False
    )

    def __repr__(self):
        return f"<Channel {self.name}>"


class User(db.Model):
    """
    A class to store the user object.

     Attributes:
        :param @id: Id to populate the database.

        :param @user_name: The user name of the user in the social network.

        :param @name: The name of the user

        :param @last_name: The last name of the user

        :param @social_network_id: The id of the social network if it has it.

        :param @channel_id: The id of the channel where the user is interacting.

        :param @channel: The channel object where the user is interacting.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    social_network_id = db.Column(db.Integer, nullable=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'),
                           nullable=False)
    channel = db.relationship('Channel', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"<User {self.user_name}>"


def get_channel_id(token):
    """
    This method finds the Channel Object using the authentication token from the channel.

     Parameters:
        :param token: the authentication token used by the channel to communicate with the system.

    Return:
        The channel object if found or None.
    """

    return Channel.query.filter_by(token=token).first()


def get_user(user_id):
    """
    This methods finds the user object by filtering by its id.

     Parameters:
        :param user_id: The id of the user.

      Return:
        The user object object if found.
    """
    current_user = User.query.filter_by(id=user_id).first()
    if current_user is not None:
        return current_user


def get_or_create_user(user, channel):
    """
    This method get an user object or creates it if it doesnt exists.

     Parameters:
        :param user: A dict containing information of the user.

        :param channel: A channel object used by the user to communicate with the system.
    """
    new_user = User.query.filter_by(user_name=user["user_name"]).first()
    if new_user is None:
        new_user = User(
            user_name=user["user_name"],
            name=user["name"],
            last_name=user["last_name"],
            channel=channel)
        if "social_network_id" in user:
            new_user.social_network_id = user["social_network_id"]

        db.session.add(new_user)
        db.session.commit()
    return new_user


def init_database():
    """
    This function is used to initially populate the database
    """
    exists = Agent.query.all()
    if exists is None or len(exists) == 0:
        agent = Agent(name='opencampuscursos')
        channel = Channel(name='@OCCChatbot', token="tokendeseguridad",
                          about="Este es el chabot de Open Campus capaz de resolver dudas sobre los diferentes cursos de la oferta actual de Open Campus",
                          social_network=SocialNetwork.telegram,
                          agent=agent)
        db.session.add(agent)
        db.session.add(channel)
        db.session.commit()

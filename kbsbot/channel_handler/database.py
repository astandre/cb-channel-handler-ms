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
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<Agent {self.name}>"


class Channel(db.Model):
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
    return Channel.query.filter_by(token=token).first()


def get_user(user_id):
    current_user = User.query.filter_by(id=user_id).first()
    if current_user is not None:
        return current_user


def get_or_create_user(user, channel):
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
        channel = Channel(name='t.me/telegramchannel', token="tokendeseguridad", social_network=SocialNetwork.telegram,
                          agent=agent)

        db.session.add(agent)
        db.session.add(channel)
        db.session.commit()

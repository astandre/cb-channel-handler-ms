import sys
from setuptools import setup, find_packages
from kbsbot.channel_handler import __version__

setup(name='channel_handler',
      description="This microservice is used to authenticate the different channels used to communicate with the chatbot.",
      long_description=open('README.rst').read(),
      version=__version__,
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      dependency_links=["https://github.com/Runnerly/flakon.git#egg=flakon"],
      install_requires=["flask", "flask_sqlalchemy", "sqlalchemy_utils", "pymongo", "requests", "cryptography"],
      author="André Herrera",
      author_ewmail="andreherrera97@hotmail.com",
      license="MIT",
      keywords=["chatbots", "microservices"],
      entry_points={
          'console_scripts': [
              'channel_handler = kbsbot.channel_handler.run:app',
          ],
      }
      )

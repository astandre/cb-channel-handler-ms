Channel Handler
===============
.. image:: https://travis-ci.org/astandre/cb-channel-handler-ms.svg?branch=master
    :target: https://travis-ci.org/astandre/cb-channel-handler-ms

.. image:: https://readthedocs.org/projects/cb-channel-handler-ms/badge/?version=latest
    :target: https://cb-channel-handler-ms.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


This microservice is used to authenticate the different channels used to communicate with the chatbot.
This microservice also communicates with the compose-engine-ms in order to retrieve the answer for the user.
Finally this microservice also stores the different users that communicate with the chatbot and the interactions between them.

This project is part of the architecture described in:
Herrera, Andre & Yaguachi, Lady & Piedra, Nelson. (2019). Building Conversational Interface for Customer Support Applied to Open Campus an Open Online Course Provider. 11-13. 10.1109/ICALT.2019.00011.


Running scripts


``docker build -t astandre/kbsbot_channel_handler . -f docker/Dockerfile``


``docker run --rm  --name=channel-handler -p 5005:8005 -it astandre/kbsbot_channel_handler``




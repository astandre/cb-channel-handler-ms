Channel Handler
===============
.. image:: https://travis-ci.org/astandre/cb-channel-handler-ms.svg?branch=master
    :target: https://travis-ci.org/astandre/cb-channel-handler-ms

.. image:: https://readthedocs.org/projects/cb-channel-handler-ms/badge/?version=latest
    :target: https://cb-channel-handler-ms.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

This project is part of the architecture described in:
Herrera, Andre & Yaguachi, Lady & Piedra, Nelson. (2019). Building Conversational Interface for Customer Support Applied to Open Campus an Open Online Course Provider. 11-13. 10.1109/ICALT.2019.00011.


Running scripts


``docker build -t astandre/kbsbot_channel_handler . -f docker/Dockerfile``


``docker run --rm  --name=channel-handler -p 5005:8005 -it astandre/kbsbot_channel_handler``




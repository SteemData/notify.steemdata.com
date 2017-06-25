Steem Notifier
==============

Send notifications for various Steem events.

Requirements
------------
- Python 3.5+
- MongoDB (on dev machine)
- Docker and Docker Compose (on production machine)

Run on development machine
--------------------------

Make sure you have a MongoDB instance running on your dev machine.

1. Create and activate new virtual env:

        python3 -m venv venv
        . venv/bin/activate


2. Install requirements:
  
        pip install -r requirements.txt


3. Open `http://localhost:5000` using your browser.


Run on production machine
-------------------------

Make sure you have [Docker](https://www.docker.com) and [Docker Compose](https://docs.docker.com/compose/) installed on the server.

1. Build the containers:

      docker-compose build

2. Run the containers:

      docker-compose up -d


Unit tests
----------

On development machine, run the following command:

      python -m unittest -b

to run the unit tests.


Open Door Policy
================

Open your garage door using your browser.


Usage
-----

Install

    pip install -r requirements/production.txt  # on Raspberry Pi or
    pip install -r requirements/dev.txt         # on development machine

set up users

    cp users_example.py users.py
    vim users.py

and run

    python server.py


HTTPS
-----

Create an SSL certificate chain

    openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.pem

and run

    python server.py --pem cert.pem

import click
import time
from flask import Flask, redirect, render_template, url_for, abort
from users import users


class Door(object):
    def __init__(self, pin):
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            self.gpio = True
        except ImportError:
            self.gpio = False

    def open(self, timeout):
        if self.gpio:
            GPIO.output(18, True)
            time.sleep(timeout)
            GPIO.output(18, False)
        else:
            print "opening door for %ds" % timeout
            time.sleep(timeout)


app = Flask(__name__)
door = Door(18)


@app.route('/')
@app.route('/<token>')
def index(token=''):
    if token not in users:
        abort(401)
    return render_template('main.html', token=token, username=users[token])


@app.route("/press/")
@app.route("/press/<token>")
def press(token=''):
    if token not in users:
        abort(401)
    door.open(3)
    return redirect(url_for('index', token=token))


@click.command()
@click.option('--pem', help='Private Key and Certificate File')
def main(pem):
    if '' in users:
        raise RuntimeError(
            "Default empty access token in users not allowed"
        )

    if pem is not None:
        import ssl
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(pem, pem)
        app.run(host='0.0.0.0', port=8000, ssl_context=context)
    else:
        app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()

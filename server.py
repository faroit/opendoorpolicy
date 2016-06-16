import click
import time
from flask import Flask, redirect, render_template, url_for


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
def index():
    return render_template('main.html')


@app.route("/press")
def press():
    door.open(3)
    return redirect(url_for('index'))


@click.command()
@click.option('--pem', help='Private Key and Certificate File')
def main(pem):
    if pem is not None:
        import ssl
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(pem, pem)
        app.run(host='0.0.0.0', port=8000, ssl_context=context)
    else:
        app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()

from flask import Flask, redirect, render_template, url_for
import time


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

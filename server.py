from flask import Flask, redirect, render_template, url_for
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')


@app.route("/press")
def open_door():
    GPIO.output(18, True)
    time.sleep(3)
    GPIO.output(18, False)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

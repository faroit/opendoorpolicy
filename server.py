from flask import Flask, render_template
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')


@app.route("/press")
def update_lamp():
    GPIO.output(18, True)
    time.sleep(3)
    GPIO.output(18, False)
    return render_template('main.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

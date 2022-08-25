from flask import Flask, render_template, Response
from shelljob import proc

from CODE import camera
from CODE.camera import Video


app = Flask(__name__)



@app.route('/mainpage')
def mainpage():
    return render_template('mainpage.html')

@app.route('/intruder')
def intruder():
    return render_template('intruder.html')


@app.route('/camera')
def camera():
    return render_template('camera.html')


@app.route('/intruder2')
def intruder2():
    return render_template('intruder2.html')



@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame +
              b'\r\n\r\n')


@app.route('/video')

def video():
    return Response(gen(Video()),
    mimetype = 'multipart/x-mixed-replace; boundary=frame')



app.run(debug=True)

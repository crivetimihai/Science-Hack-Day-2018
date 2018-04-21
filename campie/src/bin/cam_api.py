#!/usr/bin/evn/ python3

from flask import Flask, send_file
import camera

app = Flask(__name__)

@app.route('/api/pi')
def api_pi():
    cam = camera.get_image()
    response = app.response_class(
            response = cam,
            status = 200,
            mimetype = 'image/png')
    return response

if __name__ == '__main__':
    app.run('0.0.0.0',port=8080)

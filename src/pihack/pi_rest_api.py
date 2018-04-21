#!/usr/bin/env python3
"""
Displays Raspberry PI sensor data and platform information as a REST API.
"""
from flask import Flask, jsonify
from pihack import pimock

app = Flask(__name__)

@app.route('/api/pi')
def api_pi():
    pi = pimock.get_pi_mock()
    response = app.response_class(
        response = pi,
        status = 200,
        mimetype = 'application/json'
    )
    return response

if __name__ == '__main__':
        app.run('0.0.0.0', port=5000)

#!/usr/bin/env python3

##
## Sample Flask REST server implementing two methods
##
## Endpoint /api/image is a POST method taking a body containing an image
## It returns a JSON document providing the 'width' and 'height' of the
## image that was provided. The Python Image Library (pillow) is used to
## proce#ss the image
##
## Endpoint /api/add/X/Y is a post or get method returns a JSON body
## containing the sum of 'X' and 'Y'. The body of the request is ignored
##
##
from flask import Flask, request, Response
import jsonpickle
from PIL import Image
import base64
import io

# Initialize the Flask application
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
def add(a,b):
    response = {'sum' : str( a + b)}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# route http posts to this method
@app.route('/api/rawimage', methods=['POST'])
def rawimage():
    r = request
    # convert the data to a PIL image type so we can extract dimensions
    try:
        ioBuffer = io.BytesIO(r.data)
        img = Image.open(ioBuffer)
    # build a response dict to send back to client
        response = {
            'width' : img.size[0],
            'height' : img.size[1]
            }
    except:
        response = { 'width' : 0, 'height' : 0}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/dotproduct', methods=['POST'])
def dotproduct():
    try:
        body = request.get_json(force=True, silent=False)
        a = body.get('a', [])
        b = body.get('b', [])
        if not isinstance(a, list) or not isinstance(b, list):
            raise ValueError("a and b must be lists")
        if len(a) != len(b):
            raise ValueError("vectors must be the same length")
        dot = sum(float(x) * float(y) for x, y in zip(a, b))
        response = {'dot': dot}
    except Exception as e:
        response = {'error': str(e)}
    return Response(response=jsonpickle.encode(response),
                    status=200, mimetype="application/json")

# route http posts to this method
@app.route('/api/jsonimage', methods=['POST'])
def jsonimage():
    try:
        body = request.get_json(force=True, silent=False)
        img_b64 = body.get('image', '')
        if not img_b64:
            raise ValueError("missing 'image' base64 field")
        raw = base64.b64decode(img_b64, validate=True)
        img = Image.open(io.BytesIO(raw))
        response = {'width': img.size[0], 'height': img.size[1]}
    except Exception as e:
        response = {'width': 0, 'height': 0, 'error': str(e)}
    return Response(response=jsonpickle.encode(response), status=200, mimetype="application/json")

# start flask app
app.run(host="0.0.0.0", port=5055)
from flask import Flask, request, Response, jsonify
from os import environ

app = Flask(__name__)


@app.route('/<eyeTrackingURL>/<degreeOfAccuracy>/<distanceBetweenEyeTrackerAndParticipants>/'
           + '<resolutionOfScreenX>/<resolutionOfScreenY>/<sizeOfScreen>', methods=['POST'])
def sta_request(eyeTrackingURL, degreeOfAccuracy, distanceBetweenEyeTrackerAndParticipants,
               resolutionOfScreenX, resolutionOfScreenY, sizeOfScreen):
    print (request.get_data())
    print(eyeTrackingURL, degreeOfAccuracy, distanceBetweenEyeTrackerAndParticipants)
    return Response()


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
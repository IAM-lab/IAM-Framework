from flask import Flask, request, Response, jsonify
from os import environ
from Utils import utils, stringprocessing
from AOI import aoi
from Sequences import sequences
from Fixation import fixation

app = Flask(__name__)



@app.route('/<pList>/<eyeTrackingURL>/<degreeOfAccuracy>/<distanceBetweenEyeTrackerAndParticipants>/'
           + '<resolutionOfScreenX>/<resolutionOfScreenY>/<sizeOfScreen>', methods=['POST'])
def sta_request(pList, eyeTrackingURL, degreeOfAccuracy, distanceBetweenEyeTrackerAndParticipants,
                resolutionOfScreenX, resolutionOfScreenY, sizeOfScreen):
    # We receive the input body as a huge b64 encoded string separated by a \n signifying
    # the start of the segmentation file, we can split the here to pass it to our string processing
    #  function which cleans it up and allows the other modules to use it
    datafiles = request.get_data().decode("utf-8").split("\n")

    segmentation_file = stringprocessing.getSegmentationFile(datafiles[1])

    participant_files = stringprocessing.getParticipantFiles(datafiles[0])



    print(pList, eyeTrackingURL, degreeOfAccuracy, distanceBetweenEyeTrackerAndParticipants, resolutionOfScreenX,
          resolutionOfScreenY, sizeOfScreen)
    return Response()


def sta(pList, EyeTrackingFiles, EyeTrackingURL, SegmentationPath,
        degreeOfAccuracy, distanceBetweenEyeTrackerAndParticipants,
        resolutionOfScreenX, resolutionOfScreenY, sizeOfScreen):
    # STA Algorithm

    # Preliminary Stage
    myParticipants = utils.getParticipants(pList, EyeTrackingFiles, EyeTrackingURL)
    myAoIs = aoi.getAoIs(SegmentationPath)
    myErrorRateArea = utils.calculateErrorRateArea(degreeOfAccuracy, distanceBetweenEyeTrackerAndParticipants,
                                             resolutionOfScreenX, resolutionOfScreenY, sizeOfScreen)
    mySequences = sequences.createSequences(myParticipants, myAoIs, myErrorRateArea)

    keys = mySequences.keys()
    for y in range(0, len(keys)):
        mySequences[keys[y]] = mySequences[keys[y]].split('.')
        del mySequences[keys[y]][len(mySequences[keys[y]]) - 1]
    for y in range(0, len(keys)):
        for z in range(0, len(mySequences[keys[y]])):
            mySequences[keys[y]][z] = mySequences[keys[y]][z].split('-')

    # First-Pass
    mySequences_num = {}
    keys = mySequences.keys()
    for y in range(0, len(keys)):
        if (len(mySequences[keys[y]]) != 0):
            mySequences_num[keys[y]] = sequences.getNumberedSequence(mySequences[keys[y]])
        else:
            mySequences_num[keys[y]] = []

    myImportanceThreshold = utils.calculateImportanceThreshold(mySequences_num)
    myImportantAoIs = aoi.updateAoIsFlag(aoi.getNumberDurationOfAoIs(mySequences_num), myImportanceThreshold)
    myNewSequences = aoi.removeInsignificantAoIs(mySequences_num, myImportantAoIs)

    # Second-Pass
    myNewAoIList = aoi.getExistingAoIList(myNewSequences)
    myNewAoIList = fixation.calculateTotalNumberDurationofFixationsandNSV(
        myNewAoIList, fixation.calculateNumberDurationOfFixationsAndNSV(
        myNewSequences))
    myFinalList = aoi.getValueableAoIs(myNewAoIList)
    myFinalList.sort(key=lambda x: (x[4], x[3], x[2]))
    myFinalList.reverse()

    commonSequence = []
    for y in range(0, len(myFinalList)):
        commonSequence.append(myFinalList[y][0])

    return sequences.getAbstractedSequence(commonSequence)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

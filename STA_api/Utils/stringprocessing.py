import base64

def base64Decode(base64String):
    """

    :param encodedSegmentationFile:
    :return decodedFileString
    """

    return base64.b64decode(base64String)

# TODO function expects that there is a one to one match between pList and encodedParticipantFiles
# TODO i.e, participant id -> file
def getParticipantFiles(pList, encodedParticipantFiles):

    """

    :param encodedParticipantFiles:
    :return participantFileList: List containing dictionaries of decoded participant files
    """

    decodedFiles = base64.b64decode(encodedParticipantFiles)
    participantFileList = decodedFiles.decode().split("== NEW PARTICIPANT FILE ==")
    participantData = {}
    participantDataList = []

    # We are going to access participant data by key to their file, however, we first need to link the
    #  files by participant id
    participantFileIndex = 0

    # TODO Add error handling for lengths mismatch

    print(participantFileList)

    for participantId in pList:
        participantData["id"] = participantId
        participantData["eye_tracking_data"] = participantFileList[participantFileIndex]
        participantFileIndex += 1
        participantDataList.append(participantData)

    return participantDataList
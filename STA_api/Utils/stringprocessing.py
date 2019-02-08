import base64

def getSegmentationFile(encodedSegmentationFile):
    """

    :param encodedSegmentationFile:
    :return decodedFileString
    """

    return base64.b64decode(encodedSegmentationFile)


def getParticipantFiles(encodedParticipantFiles):

    """

    :param encodedParticipantFiles:
    :return participantFileList: List containing decoded participant files
    """

    decodedFiles = base64.b64decode(encodedParticipantFiles)
    participantFileList = decodedFiles.decode().split("== NEW PARTICIPANT FILE ==")

    return participantFileList
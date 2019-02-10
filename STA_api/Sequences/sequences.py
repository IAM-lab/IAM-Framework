from math import sqrt
from AOI import aoi

def createSequences(Participants, myAoIs, errorRateArea):
    """

    :param Participants:
    :param myAoIs:
    :param errorRateArea:
    :return Sequences:
    """
    Sequences = {}
    # Changed from Participant.keys() (Python 2.7 returned a list by default) to list(Participants.keys())
    keys = list(Participants.keys())

    for y in range(0, len(keys)):
        sequence = ""
        for z in range(0, len(Participants[keys[y]])):
            tempAoI = ""
            tempDuration = 0
            for k in range(0, len(myAoIs)):
                if (float(myAoIs[k][1]) - errorRateArea) <= float(Participants[keys[y]][z][3]) < ((
                        float(myAoIs[k][1]) - errorRateArea + float(myAoIs[k][2]) + 2 * errorRateArea)) and (
                        float(myAoIs[k][3]) - errorRateArea) <= float(Participants[keys[y]][z][4]) < (
                        ((float(myAoIs[k][3]) - errorRateArea) + (float(myAoIs[k][4]) + 2 * errorRateArea))):
                    tempAoI = tempAoI + myAoIs[k][5]
                    tempDuration = int(Participants[keys[y]][z][2])

            distanceList = []
            if len(tempAoI) > 1:
                # tempAoI = "(" + tempAoI + ")"
                for m in range(0, len(tempAoI)):
                    for n in range(0, len(myAoIs)):
                        if tempAoI[m] == myAoIs[n][5]:
                            distance = []
                            for s in range(int(myAoIs[n][1]), int(myAoIs[n][1]) + int(myAoIs[n][2])):
                                for f in range(int(myAoIs[n][3]), int(myAoIs[n][3]) + int(myAoIs[n][4])):
                                    distance.append(sqrt(pow(float(Participants[keys[y]][z][3]) - s, 2) + pow(
                                        float(Participants[keys[y]][z][4]) - f, 2)))
                            distanceList.append([myAoIs[n][5], min(distance)])
                distanceList.sort(key=lambda x: x[1])
                tempAoI = distanceList[0][0]

            if len(tempAoI) != 0:
                sequence = sequence + tempAoI + "-" + str(tempDuration) + "."

        print("A sequence has been created for " + keys[y])
        Sequences[keys[y]] = sequence
    return Sequences


# TODO Change references to this function to include segmentation path
def getNumberedSequence(Sequence, SegmentationPath):
    """

    :param Sequence:
    :return newSequence:
    """
    numberedSequence = [[Sequence[0][0], 1, Sequence[0][1]]]

    for y in range(1, len(Sequence)):
        if Sequence[y][0] == Sequence[y - 1][0]:
            numberedSequence.append([Sequence[y][0], numberedSequence[len(numberedSequence) - 1][1], Sequence[y][1]])
        else:
            numberedSequence.append([Sequence[y][0], getSequenceNumber(Sequence[0:y], Sequence[y][0]), Sequence[y][1]])

    AoIList = getExistingAoIListForSequence(numberedSequence)
    AoINames = aoi.getAoIs(SegmentationPath)
    AoINames = [w[5] for w in AoINames]
    newSequence = []

    myList = []
    myDictionary = {}
    replacementList = []

    for x in range(0, len(AoIList)):
        totalDuration = 0
        for y in range(0, len(numberedSequence)):
            if numberedSequence[y][0:2] == AoIList[x]:
                totalDuration = totalDuration + int(numberedSequence[y][2])
        myList.append([AoIList[x], totalDuration])

    for x in range(0, len(AoINames)):
        myAoIList = [w for w in myList if w[0][0] == AoINames[x]]
        myAoIList.sort(key=lambda x: x[1])
        myAoIList.reverse()
        if len(myAoIList) > 0:
            myDictionary[AoINames[x]] = myAoIList

    for AoI in AoIList:
        index = [w[0] for w in myDictionary[AoI[0]]].index(AoI)
        replacementList.append([AoI, [AoI[0], (index + 1)]])

    for x in range(0, len(numberedSequence)):
        myReplacementList = [w[0] for w in replacementList]
        index = myReplacementList.index(numberedSequence[x][0:2])
        newSequence.append([replacementList[index][1][0]] + [replacementList[index][1][1]] + [numberedSequence[x][2]])

    return newSequence


def getSequenceNumber(Sequence, Item):
    """

    :param Sequence:
    :param Item:
    :return:
    """
    abstractedSequence = getAbstractedSequence(Sequence)
    return abstractedSequence.count(Item) + 1


def getAbstractedSequence(Sequence):
    """

    :param Sequence:
    :return:
    """
    myAbstractedSequence = [Sequence[0][0]]
    for y in range(1, len(Sequence)):
        if myAbstractedSequence[len(myAbstractedSequence) - 1] != Sequence[y][0]:
            myAbstractedSequence.append(Sequence[y][0])
    return myAbstractedSequence


def getExistingAoIListForSequence(Sequence):
    """

    :param Sequence:
    :return:
    """
    AoIlist = []
    for x in range(0, len(Sequence)):
        try:
            AoIlist.index(Sequence[x][0:2])
        except:
            AoIlist.append(Sequence[x][0:2])
    return AoIlist

def getAoIs(SegmentationString):
    """

    :param Path:
    :return:
    """
    AoIs = []
    mySegments = SegmentationString.decode().split('\n')

    # New empty line gets split too, hence we ignore it
    for x in range(0, len(mySegments)-1):
        temp = mySegments[x].split(' ')
        AoIs.append([temp[0], temp[1], temp[2], temp[3], temp[4], temp[5]])

    return AoIs


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


def getNumberDurationOfAoIs(Sequences):
    """

    :param Sequences:
    :return:
    """
    AoIs = getExistingAoIList(Sequences)
    AoIcount = []
    for x in range(0, len(AoIs)):
        counter = 0
        duration = 0
        flagCounter = 0
        keys = list(Sequences.keys())
        for y in range(0, len(keys)):
            if [s[0:2] for s in Sequences[keys[y]]].count(AoIs[x]) > 0:
                counter = counter + [s[0:2] for s in Sequences[keys[y]]].count(AoIs[x])
                duration = duration + sum([int(w[2]) for w in Sequences[keys[y]] if w[0:2] == AoIs[x]])
                flagCounter = flagCounter + 1

        if flagCounter == len(keys):
            AoIcount.append([AoIs[x], counter, duration, True])
        else:
            AoIcount.append([AoIs[x], counter, duration, False])
    return AoIcount


def updateAoIsFlag(AoIs, threshold):
    """

    :param AoIs:
    :param threshold:
    :return:
    """
    for AoI in AoIs:
        if AoI[1] >= threshold[0] and AoI[2] >= threshold[1]:
            AoI[3] = True
    return AoIs


def removeInsignificantAoIs(Sequences, AoIList):
    """

    :param Sequences:
    :param AoIList:
    :return:
    """
    significantAoIs = []
    for AoI in AoIList:
        if AoI[3]:
            significantAoIs.append(AoI[0])

    keys = list(Sequences.keys())
    for y in range(0, len(keys)):
        temp = []
        for k in range(0, len(Sequences[keys[y]])):
            try:
                significantAoIs.index(Sequences[keys[y]][k][0:2])
                temp.append(Sequences[keys[y]][k])
            except:
                continue
        Sequences[keys[y]] = temp
    return Sequences


def getExistingAoIList(Sequences):
    """

    :param Sequences:
    :return: List containing areas of interest found previously
    """
    AoIlist = []
    keys = list(Sequences.keys())
    for y in range(0, len(keys)):
        for x in range(0, len(Sequences[keys[y]])):
            try:
                AoIlist.index(Sequences[keys[y]][x][0:2])
            except:
                AoIlist.append(Sequences[keys[y]][x][0:2])
    return AoIlist


def getValueableAoIs(AoIList):
    """

    :param AoIList: A list containing the polygons defining areas of interest on the page
    :return: Returns a list of valuable areas of interest
    """
    commonAoIs = []
    valuableAoIs = []
    for myAoIdetail in AoIList:
        if myAoIdetail[5] == True:
            commonAoIs.append(myAoIdetail)

    minValue = commonAoIs[0][4]
    for AoIdetails in commonAoIs:
        if minValue > AoIdetails[4]:
            minValue = AoIdetails[4]

    for myAoIdetail in AoIList:
        if myAoIdetail[4] >= minValue:
            valuableAoIs.append(myAoIdetail)

    return valuableAoIs

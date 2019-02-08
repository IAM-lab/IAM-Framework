def calculateNumberDurationOfFixationsAndNSV(Sequences):
    """

    :param Sequences:
    :return Sequences:
    """
    keys = Sequences.keys()
    for x in range(0, len(keys)):
        myAbstractedSequence = []
        myAbstractedSequence = [Sequences[keys[x]][0][0:2] + [1] + [int(Sequences[keys[x]][0][2])]]
        for y in range(1, len(Sequences[keys[x]])):
            if myAbstractedSequence[len(myAbstractedSequence) - 1][0:2] != Sequences[keys[x]][y][0:2]:
                myAbstractedSequence.append(Sequences[keys[x]][y][0:2] + [1] + [int(Sequences[keys[x]][y][2])])
            else:
                myAbstractedSequence[len(myAbstractedSequence) - 1][2] = myAbstractedSequence[len(myAbstractedSequence)
                                                                                              - 1][2] + 1
                myAbstractedSequence[len(myAbstractedSequence) - 1][3] = \
                    myAbstractedSequence[len(myAbstractedSequence) - 1][3] + int(Sequences[keys[x]][y][2])

        Sequences[keys[x]] = myAbstractedSequence

    keys = Sequences.keys()
    for x in range(0, len(keys)):
        for y in range(0, len(Sequences[keys[x]])):
            if len(Sequences[keys[x]]) < 2:
                value = 0
            else:
                value = 0.9 / (len(Sequences[keys[x]]) - 1)
            NSV = 1 - round(y, 2) * value
            Sequences[keys[x]][y] = Sequences[keys[x]][y] + [NSV]
    return Sequences


def calculateTotalNumberDurationofFixationsandNSV(AoIList, Sequences):
    """

    :param AoIList:
    :param Sequences:
    :return AoIList:
    """
    for x in range(0, len(AoIList)):
        duration = 0
        counter = 0
        totalNSV = 0

        flag = 0
        keys = Sequences.keys()
        for y in range(0, len(keys)):
            for k in range(0, len(Sequences[keys[y]])):
                if Sequences[keys[y]][k][0:2] == AoIList[x]:
                    counter = counter + Sequences[keys[y]][k][2]
                    duration = duration + Sequences[keys[y]][k][3]
                    totalNSV = totalNSV + Sequences[keys[y]][k][4]
                    flag = flag + 1
        if flag == len(Sequences):
            AoIList[x] = AoIList[x] + [counter] + [duration] + [totalNSV] + [True]
        else:
            AoIList[x] = AoIList[x] + [counter] + [duration] + [totalNSV] + [False]

    return AoIList

from math import tan, radians, sqrt
from AOI import aoi

# TODO Fix function to use string list
def getParticipants(pList, Path, pageName):
    Participants = {}
    for x in pList:
        fo = open (Path + "P" + str(x) + ".txt", "r")
        myFile = fo.read()
        myRecords = myFile.split('\n')
        myRecords_templist = []

        for y in range (1, len(myRecords) - 1):
            try:
                if myRecords[y].index(pageName) > 0:
                    myRecords_templist.append(myRecords[y].split('\t'))
            except:
                continue
        if x > 9:
            Participants["P" + str(x)] = myRecords_templist
        else:
            Participants["P0" + str(x)] = myRecords_templist
    return Participants


def calculateErrorRateArea(accuracy_degree, distance, screen_resolution_x, screen_resolution_y, screen_diagonal_size):
    """

    :param accuracy_degree:
    :param distance:
    :param screen_resolution_x:
    :param screen_resolution_y:
    :param screen_diagonal_size:
    :return Error rate rounded to 2 decimal places:
    """
    error_rate_area_in_c_m = tan(radians(accuracy_degree)) * distance
    error_rate_area_in_pixels = (error_rate_area_in_c_m * getPPI(screen_resolution_x, screen_resolution_y,
                                                                 screen_diagonal_size)) / 2.54
    return round(error_rate_area_in_pixels, 2)


def getPPI(screen_resolution_x, screen_resolution_y, screen_diagonal_size):
    """

    :param screen_resolution_x:
    :param screen_resolution_y:
    :param screen_diagonal_size:
    :return:
    """
    diagonal_resolution = sqrt(pow(screen_resolution_x, 2) + pow(screen_resolution_y, 2))
    PPI = diagonal_resolution / screen_diagonal_size
    return PPI


def calculateImportanceThreshold (mySequences):
    myAoICounter = aoi.getNumberDurationOfAoIs(mySequences)
    commonAoIs = []
    for myAoIdetail in myAoICounter:
        if myAoIdetail[3]:
            commonAoIs.append(myAoIdetail)

    # TODO This doesn't look good, should throw exception and exit gracefully
    if len(commonAoIs) == 0:
        print ("No shared instances!")
        exit(1)

    minValueCounter = commonAoIs[0][1]
    for AoIdetails in commonAoIs:
        if minValueCounter > AoIdetails[1]:
            minValueCounter = AoIdetails[1]

    minValueDuration = commonAoIs[0][2]
    for AoIdetails in commonAoIs:
        if minValueDuration > AoIdetails[2]:
            minValueDuration = AoIdetails[2]

    return [minValueCounter, minValueDuration]

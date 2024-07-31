import math

def printOpt1(baseCount, antennaCount, maxAnts, minAnts,strAvg, singleAntPt,multiAntPt, allPoints, coveredPoints,qg, antPPS, coveredArea, baseJ,antennaJ):

    print("The total number of base stations = "+str(baseCount))
    print("The total number of antennas = "+str(antennaCount))
    print("The max, min and average of antennas per BS = "+str(maxAnts)+", "+str(minAnts)+", "+strAvg)
    print("The total number of points covered by exactly one antenna = "+str(singleAntPt))
    print("The total number of points covered by more than one antenna = "+ str(multiAntPt))
    print("The total number of points not covered by any antenna = "+str(len(allPoints) - len(coveredPoints)))
    print("The maximum number of antennas that cover one point: "+str(qg))
    print("The average number of antennas covering a point: "+antPPS)
    print("The percentage of the covered area = 100x"+str(len(coveredPoints))+"/"+str(len(allPoints))+" = "+coveredArea+"%")
    print("The id of the base station and antenna covering the maximum number of points = base station "+str(baseJ)+", antenna "+str(antennaJ))
def baseStats(bases, id, allPoints):
    allPointslen = len(allPoints)
    antennas = []
    antennaCount = 0
    baseChosen = {}
    for x in bases:
        if(x["id"] == id):
            baseChosen.update(x)

    
    antenna = baseChosen["ants"]

    amountOfPoints =0

    pointComare = []
    coveredPoints = set()
    IDA = 0
    bigIDA = 0
    for x in antenna:
        pointsPerAntenna = set()
        temp = x["pts"]
        antennaID = x["id"]
        antennaIDsize = set()
        
        for y in temp:
            amountOfPoints += 1
            temporary = (y[0], y[1])
            antennaIDsize.add(temporary)
            coveredPoints.add(temporary)
            pointsPerAntenna.add(temporary)
        pointComare.append(pointsPerAntenna)
        if(len(antennaIDsize)> bigIDA):
            bigIDA = len(antennaIDsize)
            IDA = int(antennaID)
    maxPointsPA = 0

    intersect = pointComare[0]
    
    for x in range(1,antennaCount):
        diff = intersect.intersection(pointComare[x])
        joint = intersect.union(pointComare[x])
        intersect = joint - diff
    

    for x in coveredPoints:
        size = 0
        
        for y in pointComare:
            for z in y:
                if(z == x):
                    size +=1
        if(size>maxPointsPA):
            maxPointsPA = size
            
        
    
    antennaCount = len(antenna)
    avgAntennaPP = amountOfPoints/len(coveredPoints)
    avgPPstr = format(avgAntennaPP, ".1f")

    

    perc = (len(coveredPoints)*100)/len(allPoints)
    percStr = format(perc, ".1f")
    
    print("The total number of antennas: "+str(antennaCount))
    print("The total number of points covered by exactly one antenna: "+str(len(intersect)))
    print("The total number of points covered by more than one antenna: "+str(len(coveredPoints)-len(intersect)))
    print("The total number of points not covered by any antenna: "+str(allPointslen - amountOfPoints))
    print("The maximum number of antennas that cover one point: "+str(maxPointsPA))
    print("The average of antennas covering a point: "+avgPPstr)
    print("The percentage of the covered area by the base station: "+percStr+"%")
    print("The id of the antenna that covers the maximum number of points: "+str(IDA))
    
def coverage(uLat, uLon,bases):
    
    userEntry = (uLat, uLon)
    check = 0

    for x in bases:

        tBaseId = x["id"]
        tAntId = ""
       
        tempAnt =  x["ants"]
        
        for y in tempAnt:
            tAntId = y["id"]
            

            tempPts = y["pts"]

            for z in tempPts:

                current = (z[0],z[1])
                if (current == userEntry):
                    check += 1
                    print("This point is covered in station "+ str(tBaseId)+ ", in antenna "+str(tAntId)+" and the power received is "+str(z[2]))

    if (check == 0):
        
        sameDistance = []

        distance = -1.0

        for x in bases:
             tBaseId = x["id"]
             tAntId = ""
             tAntLat = x["lat"]
             tAntLon = x["lon"]
             tempAnt =  x["ants"]
            
             for y in tempAnt:
                tAntId = y["id"]

                tempPts = y["pts"]

                for z in tempPts:

                    lat = z[0]
                    lon = z[1]

                    phi = uLat - lat
                    lamda = uLon - lon
                    dis = math.sqrt((phi*phi)+(lamda *lamda))
                    
                    if (distance == -1):

                        distance = dis
                        sameDistance.append([str(tBaseId), str(tAntId), "Latitude is "+str(lat)+", longitude is "+str(lon)])
                    elif(distance > dis):
                        distance = dis
                        sameDistance = [[str(tBaseId), str(tAntId), "Latitude is "+str(lat)+", longitude is "+str(lon)]]
                    elif(distance == dis):
                        sameDistance.append([str(tBaseId), str(tAntId), "Latitude is "+str(lat)+", longitude is "+str(lon)])
                    
        distance = format(distance, ".3f")
        print("The nearest stations with a distance of "+ distance+" are:")
        for x in sameDistance:
            print("Station "+x[0]+", antenna "+x[1]+", "+x[2])
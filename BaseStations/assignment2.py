import sys
import json
from functions import *
import random

baseCount =0
antennaCount = 0
pointsCount = 0
coveredArea = 0.0
averageAntenna =0.0
singleAntPt =0
multiAntPt = 0
antennaPoints = 0

check =0
try:
    file = open(sys.argv[1])
except:
    print("\nError opening file. Aborting...\n")
    exit()

try:
    data = json.load(file)
except:
    print("\nError loading .json file\n")
    exit()


#Reading latitudes and getting total points
try:
    min_lat = data["min_lat"]
    max_lat = data["max_lat"]
    min_lon = data["min_lon"]
    max_lon = data["max_lon"]
    steps = data["step"]
    totalPoints = int(round(((max_lat -min_lat)/steps)*((max_lon- min_lon)/steps)))
except:
    print("\nError in latitude, longitude or steps from .json file. Aborting...\n")
    exit()
allPoints = set()
coveredPoints = set()

for x in range(round((max_lat - min_lat)/steps)+1):
    
    
    for y in range(round((max_lon - min_lon)/steps)+1):
        xtemp =0
        ytemp = 0
        if (max_lat < 0):
            xtemp = round(min_lat) - x*steps
        else:
            xtemp = round(min_lat) + x*steps
        
        if(max_lon < 0):
          ytemp = round(min_lon) - y*steps  
        else:
            ytemp = round(min_lon) + y*steps
        
       


        allPoints.add((xtemp,ytemp))

totalPoints = len(allPoints)





# Counting Bases
try:
    bases = data["baseStations"]
except:
    print("\nError reading \"baseStation\" from .json file. Aborting...\n")
    exit()
baseCount = len(bases)
antennas = []
points = []

#Counting antennas
try:
    temporary = bases[0]["ants"]
except:
    print("Error reading \"ants\" value from .json")
    exit()

minAnts = len(temporary)
maxAnts = len(temporary)
incrementer = 0

baseJ = ""
antennaJ = ""
sizeJ =0
stationIDs = []
try:
    for x in bases:
        
        tempAID = 0
        temporary = bases[incrementer]["ants"]
        tempBID = bases[incrementer]["id"]
        stationIDs.append(tempBID)
        if (minAnts>len(temporary)):
            minAnts = len(temporary)
        elif (maxAnts<len(temporary)):
            maxAnts = len(temporary)

        incrementer +=1
        atemp = x["ants"]
    
        
        
        
        for y in atemp:
            
            tempAID = y["id"]
            sizeID = len(y["pts"])
            if (sizeID>sizeJ):
                baseJ = tempBID
                antennaJ = tempAID
                sizeJ = sizeID
            antennas.append(y)
    
except:
    print("\nError reading values from .json file. Aborting...\n")
    exit()

try:
    for x in antennas:
        
        
        ptemp = x["pts"]
        points.append(ptemp)
except:
    print("Error reading \"ants\" value from .json")
    exit()


pointCompare = []
try:
    for x in points:
        single = set()
        for y in x:
            antennaPoints += 1
            temp = (y[0], y[1])
            single.add(temp)
            coveredPoints.add(temp)

        pointCompare.append(single)
except:
    print("Error reading \"pts\" value from .json")
    exit()

intersect = pointCompare[0]
antennaCount = len(antennas)
pointsCount = len(points)
diffPoints= set()

for x in range(1,len(pointCompare),1):
    
    diff = intersect.intersection(pointCompare[x])
    for c in diff:
        diffPoints.add(c)
    joint = intersect.union(pointCompare[x])
    intersect = joint - diff
qg = 0
for x in diffPoints:
    size =0

    for y in pointCompare:
        for z in y:
            if(x == z):
                size+=1
    
    if (size>qg):
        qg = size

singleAntPt = len(intersect)


coveredArea = (len(coveredPoints)/len(allPoints))*100

multiAntPt = len(coveredPoints) - singleAntPt


averageAntenna = antennaCount/baseCount

strAvg = format(averageAntenna, ".1f")

coveredArea = format(coveredArea, ".2f")




file.close()
try:
    antPP = antennaPoints/ len(coveredPoints)

except:
    print("Error with values from .json file. Aborting...")
    exit()
antPPS = format(antPP, ".1f")
#printOpt1(baseCount, antennaCount, maxAnts, minAnts,strAvg, singleAntPt,multiAntPt, allPoints, coveredPoints,qg,antPPS, coveredArea, baseJ, antennaJ)
user = 0.0



while(user != 4):
    print("\n1. Display Global Statistics")
    print("2. Display Statistics")
    print("     2.1. Statistics for a random station")
    print("     2.2. Choose a station by Id")
    print("3. Check Coverage")
    print("4. Exit")
    print("\nEnter your choice: ", end='')
    try:
        user = float(input())
    except:
        user = 5
    
    if(user == 1):
        print("")
        printOpt1(baseCount, antennaCount, maxAnts, minAnts,strAvg, singleAntPt,multiAntPt, allPoints, coveredPoints,qg,antPPS, coveredArea, baseJ, antennaJ)

    elif (user ==2.1):
        print('')
        rndm = random.choice(stationIDs)
        print("BaseStation "+str(rndm)+":\n")
        
        baseStats(bases,rndm, allPoints)
    elif (user == 2.2):
        print("Enter the id of the station you wish to see: ",end='')
        try:
            id = int(input())
            print("")
            baseStats(bases, id, allPoints)
        except:
            print("Invalid entry. Try Again")
            continue

       

    elif (user == 3):
        print("Please enter a Latitude: ", end='')
        try:
            uLat = float(input())
            print("Please enter a Latitude: ", end='')
            uLon = float(input())
        except:
            print("Invalid entry try again\n")
            continue
        

        coverage(uLat,uLon, bases)

    elif (user == 4):
        print("Thank you for using my program, have a great day!")
    else:
        print("Invalid entry, try again\n")
        
    
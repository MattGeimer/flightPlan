import math

TFDTC = [[74,730,0,0,0], [73,695,1,.4,2], [73,655,3,.8,4], [73,620,4,1.2,6], [73,600,6,1.5,8], [73,550,8,1.9,10], [73,505,10,2.2,13],
 [73,455,12,2.6,16], [72,410,14,3.0,19], [72,360,17,3.4,22], [72,315,20,3.9,27], [72,265,24,4.4,32], [72,220,28,5.0,38]]
def climbPerf(startingAltitude,endingAltitude):
    climbSpeed = (TFDTC[startingAltitude][0]+TFDTC[endingAltitude][0]) / 2
    climbRate = (TFDTC[startingAltitude][1] + TFDTC[endingAltitude][1]) / 2
    timeToClimb = TFDTC[endingAltitude][2]-TFDTC[startingAltitude][2]
    fuelUsedToClimb = TFDTC[endingAltitude][3]-TFDTC[startingAltitude][3]
    fuelUsedToClimb = int(fuelUsedToClimb*100)/100
    distanceToClimb = TFDTC[endingAltitude][4]-TFDTC[startingAltitude][4]
    output = []
    output = [climbSpeed, climbRate, timeToClimb, fuelUsedToClimb, distanceToClimb]
    return output

def windCorrectionCalc(trueCourse, trueAirSpeed, windDirection, windVelocity):
    #Find the vector of wind b/c wind is given FROM not TO
    if(windDirection <= 180):
        windVector = windDirection + 180
    else:
        windVector = windDirection - 180

    #Find the angle between trueCourse and windVector and change to radians
    if(trueCourse == windVector):
            windMagic = 0
    elif(trueCourse > windVector):
        windMagic = trueCourse - windVector
    else:
        windMagic = windVector - trueCourse
    windMagic = math.radians(windMagic)
    #Find the y component of wind vector
    windCorrectionForce = windVelocity * math.sin(windMagic)
    #Find the x component of wind vector
    windCorrectedSpeed = windVelocity * math.cos(windMagic)
    #Find the groundSpeed
    groundSpeed = windCorrectedSpeed + trueAirSpeed
    #Round groundSpeed
    groundSpeed = int(groundSpeed*10)/10
    #Find the angle to adjust for wind and fly trueCourse
    windCorrectionAngle = math.atan(windCorrectionForce / groundSpeed)
    #Convert windCorrectionAngle to degrees and round
    windCorrectionAngle = math.degrees(windCorrectionAngle)
    windCorrectionAngle = int(windCorrectionAngle*10)/10
    output = [windCorrectionAngle, groundSpeed]
    return output
legs = eval(input("Enter number of legs: "))
routeData = []
departureAltitude = eval(input("Enter departure airport altitude: "))
lastAltitude = int(departureAltitude / 1000)
trueAirSpeed = eval(input("Enter Cruise True Air Speed: "))
fuelConsumptionPerMinute = eval(input("Enter fuel consumption in gallons per hour: ")) / 60
print('\n')

for i in range(0,legs):
    print('\n')
    print("Leg " + str(i + 1) + '\n')
    trueCourse = eval(input("Enter true course: "))
    altitude = eval(input("Enter altitude for leg: "))
    distance = eval(input("Enter distance for leg: "))
    altitude = int(altitude/1000)
    if(i > 0):
        if(altitude != lastAltitude):
            climbPerformance = []
            climbPerformance = climbPerf(lastAltitude, altitude)
            routeData.append([trueCourse, climbPerformance[0], 0, 0, 0, altitude, climbPerformance, 0, 0, 0, 0, climbPerformance[4], 0, 0])
            distance = distance - climbPerformance[4]
    elif(i==0):
        climbPerformance = []
        climbPerformance = climbPerf(lastAltitude, altitude)
        routeData.append([trueCourse, climbPerformance[0], 0, 0, 0, altitude, climbPerformance, 0, 0, 0, 0, climbPerformance[4], 0, 0])
        distance = distance - climbPerformance[4]

    #routeData [trueCourse, trueAirSpeed, windDirection, windVelocity, magneticVariation, altitude, climbPerformance (if applicable), groundSpeed, trueHeading, magneticHeading, courseHeading, distance, estimatedTimeEnroute]
    '''
    routeData Index:
    0: trueCourse
    1: trueAirSpeed
    2: windDirection
    3: windVelocity
    4: magneticVariation
    5: altitude
    6: climbPerformance (If applicable)
    7: groundSpeed
    8: trueHeading
    9: magneticHeading
    10: courseHeading
    11: distance
    12: estimatedTimeEnroute
    13: estimatedFuelConsumption
    '''
    routeData.append([trueCourse, trueAirSpeed, 0, 0, 0, altitude, 0, 0, 0, 0, 0, distance, 0, 0])
    lastAltitude = altitude

print('\n')
windChanges = eval(input("Enter number of wind changes: "))
if(windChanges > 0 and windChanges <= legs):
    windLegIndex = 0
    for i in range(0,windChanges + 1):
        windDirection = eval(input("Enter wind direction: "))
        windVelocity = eval(input("Enter wind speed: "))
        if(i == windChanges):
            lastLegWind = legs - windLegIndex
        else:
            lastLegWind = eval(input("Enter the number of legs the wind is the same: ")) + windLegIndex
        for j in range(windLegIndex, lastLegWind + windLegIndex):
            routeData[j][2] = windDirection
            routeData[j][3] = windVelocity
        windLegIndex = lastLegWind
else:
    windDirection = eval(input("Enter wind direction: "))
    windVelocity = eval(input("Enter wind speed: "))
    for i in range(0,len(routeData)):
        routeData[i][2] = windDirection
        routeData[i][3] = windVelocity

magneticVariationChanges = eval(input("Enter number of Magnetic Variation changes: "))
if(magneticVariationChanges > 0 and magneticVariationChanges <= legs):
    magneticVariationLegIndex = 0
    for i in range(0,magneticVariationChanges + 1):
        magneticVariation = eval(input("Enter Magnetic Variation (with '+' for West and '-' for East): "))
        if(magneticVariation[0] == '+'):
            magneticVariation = int(magneticVariation[1])
        else:
            magneticVariation = int(magneticVariation[1])*-1
        if(i == magneticVariationChanges):
            lastLegMagneticVariation = legs - magneticVariationLegIndex
        else:
            lastLegMagneticVariation = eval(input("Enter the number of legs the Magnetic Variation is the same: ")) + magneticVariationLegIndex
        for j in range(magneticVariationLegIndex, lastLegMagneticVariation + magneticVariationLegIndex):
            routeData[j][4] = magneticVariation
        magneticVariationLegIndex = lastLegMagneticVariation
else:
    magneticVariation = eval(input("Enter Magnetic Variation (with '+' for West and '-' for East): "))
    for i in range(0,len(routeData)):
        routeData[i][4] = magneticVariation

print('\n')
windCorrectionData = []
for i in range(0,len(routeData)):
    windCorrectionData = windCorrectionCalc(routeData[i][0], routeData[i][1], routeData[i][2], routeData[i][3])
    routeData[i][7] = windCorrectionData[1]
    routeData[i][8] = windCorrectionData[0] + routeData[i][0]
    routeData[i][9] = routeData[i][8] + routeData[i][4]
    routeData[i][10] = routeData[i][9] + 0 #0 is deviation from aircraft equipment
    routeData[i][12] = int(routeData[i][11] / routeData[i][7] * 6000)/100
    if(routeData[i][6] == 0):
        routeData[i][13] = fuelConsumptionPerMinute * routeData[i][12]
    else:
        routeData[i][13] = routeData[i][6][3]

print("Number of legs including climbs: " + str(len(routeData)))
for i in range(0,3):
    print('\n')
'''
routeData Index:
0: trueCourse
1: trueAirSpeed
2: windDirection
3: windVelocity
4: magneticVariation
5: altitude
6: climbPerformance (If applicable)
7: groundSpeed
8: trueHeading
9: magneticHeading
10: courseHeading
11: distance
12: estimatedTimeEnroute
13: estimatedFuelConsumption
'''
totalDistance = 0
totalFuel = 0
totalTime = 0
for i in range(0,len(routeData)):
    totalDistance = totalDistance + routeData[i][11]
    totalFuel = totalFuel + routeData[i][13]
    totalTime = totalTime + routeData[i][12]
    print("Leg " + str(i + 1) + ":" + '\n' + '\n')
    print("Altitude: " + str(routeData[i][5]))
    print("Wind Direction: " + str(routeData[i][2]))
    print("Wind Velocity: " + str(routeData[i][3]))
    print("True Airspeed: " + str(routeData[i][1]))
    print("True Course: " + str(routeData[i][0]))
    print("Wind Correction Angle: " + str(int((routeData[i][8] - routeData[i][0]) * 10) / 10))
    print("True Heading: " + str(routeData[i][8]))
    print("Magnetic Variation: " + str(routeData[i][4]))
    print("Magnetic Heading: " + str(routeData[i][9]))
    print("Deviation: " + str(0))
    print("Course Heading: " + str(routeData[i][10]))
    print("Ground Speed: " + str(routeData[i][7]))
    print("Distance: " + str(routeData[i][11]))
    print("Estimated Time Enroute: " + str(routeData[i][12]))
    print("Estimated Fuel Consumption: " + str(routeData[i][13]))
    print('\n')
totalDistance = int(totalDistance*10)/10
totalFuel = int(totalFuel*10)/10
totalTime = int(totalTime*10)/10
print('\n' + "Total Trip: " + '\n' + '\n')
print("Total Distance: " + str(totalDistance))
print("Estimated Total Time Enroute: " + str(totalTime))
print("Estimated Total Fuel Consumption: " + str(totalFuel))

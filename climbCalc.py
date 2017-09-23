print("FlightPlan Beta" + '\n' + "This TOOL should NOT be the sole means of planning a flight")
#Time Fuel and Distance data: (Matrix_Arg_1*1000=Pressure_Alt)
TFDTC = [[74,730,0,0,0], [73,695,1,.4,2], [73,655,3,.8,4], [73,620,4,1.2,6], [73,600,6,1.5,8], [73,550,8,1.9,10], [73,505,10,2.2,13],
 [73,455,12,2.6,16], [72,410,14,3.0,19], [72,360,17,3.4,22], [72,315,20,3.9,27], [72,265,24,4.4,32], [72,220,28,5.0,38]]
def climbPerf(startingAltitude,endingAltitude):
    print("To Reach " + str(endingAltitude*1000) + "ft from " + str(startingAltitude*1000) + "ft: ")
    climbSpeed = (TFDTC[startingAltitude][0]+TFDTC[endingAltitude][0]) / 2
    print("Climb Speed: " + str(climbSpeed))
    climbRate = (TFDTC[startingAltitude][1] + TFDTC[endingAltitude][1]) / 2
    print("Rate of Climb in FPM: " + str(climbRate))
    timeToClimb = TFDTC[endingAltitude][2]-TFDTC[startingAltitude][2]
    print("Time to reach " + str(endingAltitude*1000) + "ft from starting altitude: " + str(timeToClimb) + " minutes")
    fuelUsedToClimb = TFDTC[endingAltitude][3]-TFDTC[startingAltitude][3]
    fuelUsedToClimb = int(fuelUsedToClimb*100)/100
    print("Fuel required to reach " + str(endingAltitude*1000) + "ft from starting altitude: " + str(fuelUsedToClimb) + " gallons")
    distanceToClimb = TFDTC[endingAltitude][4]-TFDTC[startingAltitude][4]
    print(str(distanceToClimb) + "nm are required to climb to " + str(endingAltitude*1000) + "ft from starting altitude" + '\n')


startingAltitude=int(eval(input("Enter pressure altitude of departure airport (Round by thousands): "))/1000)
print('\n')
for i in range(0,eval(input("Enter how many step climbs to calculate: "))):
    endingAltitude=int(eval(input("Enter altitude of end of climb (Round by thousands): "))/1000)
    climbPerf(startingAltitude,endingAltitude)
    startingAltitude=endingAltitude
    print("\n")

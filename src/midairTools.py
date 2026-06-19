import math

class Midair:
    def __init__(self):
        self.airDrag = 0.9800000190734863
        self.gravity = 0.04

def barrelCalc(powerX, powerY, powerZ, projX, projY, projZ):
    deltaX = powerX - projX
    deltaY = powerY - projY
    deltaZ = powerZ - projZ

    distance = math.sqrt(deltaX**2 + deltaY**2 + deltaZ**2)

    efficiencyX = deltaX / distance
    efficiencyY = deltaY / distance
    efficiencyZ = deltaZ / distance

    distanceEfficiency = 1 - distance / 8

    return efficiencyX, efficiencyY, efficiencyZ, distanceEfficiency

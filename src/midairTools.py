import math

airDrag = 0.9800000190734863
gravity = 0.04
headBlock = 0.019999980926514

def barrelCalc(powerX, powerY, powerZ, projX, projY, projZ):
    deltaX = projX - powerX
    deltaY = projY - powerY
    deltaZ = projZ - powerZ

    distance = math.sqrt(deltaX**2 + deltaY**2 + deltaZ**2)

    efficiencyX = deltaX / distance
    efficiencyY = deltaY / distance
    efficiencyZ = deltaZ / distance

    distanceEfficiency = 1 - distance / 8

    return efficiencyX, efficiencyY, efficiencyZ, distanceEfficiency

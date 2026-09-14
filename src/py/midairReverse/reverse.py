#Impossible :(

from src.py.midairTools import barrelCalc, airDrag, gravity, headBlock
import json

with open("src/py/decimalPosition.json", "r") as f:
    decimalPosition = json.load(f)

for blockName, offset in decimalPosition["north"].items():
    print(f"=== {blockName} ===")

    powerSandX, powerSandY, powerSandZ = 367879.50999999046, 6.0, -396762.50999999046
    powerReverseX, powerReverseY, powerReverseZ = 367879.50999999046, 6.0, -396762.50999999046
    sandX, sandY, sandZ = 367878 + offset, 6.519999980926515, -396763.49000000954
    reverseX, reverseY, reverseZ = 367878 + offset, 6.519999980926514, -396763.49000000954

    heightAdjustY = 25 + headBlock

    tntAmount = 234
    gametickMax = 24

    diffGametick = 4

    axis = "z"

    tntLimit = 5000
    direction = "north"

    sandEfficiencyX, sandEfficiencyY, sandEfficiencyZ, sandDistanceEfficiency = barrelCalc(powerSandX, powerSandY, powerSandZ, sandX, sandY, sandZ)
    reverseEfficiencyX, reverseEfficiencyY, reverseEfficiencyZ, reverseDistanceEfficiency = barrelCalc(powerReverseX, powerReverseY, powerReverseZ, reverseX, reverseY, reverseZ)

    def calcRatio(sandEfficiency, reverseEfficiency, projSand, projReverse):
        for i in range(tntAmount):
            rangeSandValue = sandEfficiency * sandDistanceEfficiency * i
            rangeSandTotal = rangeSandValue + projSand

            rangeSandValueY = 0.0
            rangeSandTotalY = heightAdjustY 

            for j in range(2, gametickMax):
                rangeSandValue *= airDrag
                rangeSandTotal += rangeSandValue
                velocity = rangeSandValue * airDrag

                rangeSandValueY -= gravity
                rangeSandTotalY += rangeSandValueY
                rangeSandValueY *= airDrag

                if 0 < rangeSandTotal % 1 < 1:

                    for k in range(1, i):
                        rangeReverseValue = reverseEfficiency * reverseDistanceEfficiency * k
                        rangeReverseTotal = rangeReverseValue + projReverse

                        rangeReverseValueY = 0.0
                        rangeReverseTotalY = heightAdjustY

                        for l in range(2, j + diffGametick+1):
                            rangeReverseValue *= airDrag
                            rangeReverseTotal += rangeReverseValue

                            rangeReverseValueY -= gravity
                            rangeReverseTotalY += rangeReverseValueY
                            rangeReverseValueY *= airDrag

                        if sandEfficiency > 0:
                            behind = rangeReverseTotal - rangeSandTotal
                        else:
                            behind = rangeSandTotal - rangeReverseTotal

                        if 0 <= behind <= 4:

                            _, ratioReverseEfficiencyY, ratioReverseEfficiencyZ, ratioReverseDistanceEfficiency = barrelCalc(1, rangeReverseTotalY, rangeReverseTotal, 1, rangeSandTotalY, rangeSandTotal)
                            
                            bestReverse = None
                            bestDiff = float("inf")

                            for m in range(tntLimit):
                                velocityReverse = ratioReverseEfficiencyZ * ratioReverseDistanceEfficiency * m

                                velocityFinal = velocityReverse + velocity

                                diff = abs(velocityFinal)

                                if diff < bestDiff:
                                    bestDiff = diff
                                    bestReverse = m
                            
                            velocitySandY = ratioReverseEfficiencyY * ratioReverseDistanceEfficiency * bestReverse
                            velocityFinalY = rangeSandTotalY + velocitySandY + rangeSandValueY

                            if bestDiff < 0.0001:

                                print("SAND")
                                print(f"Distance {rangeSandTotal} | Power {i} | Gametick {j} | Y {rangeSandTotalY} | Block {abs(rangeSandTotal - projSand)} | Velocity {velocity} ")
                                print("REVERSE")
                                print(f"Distance {rangeReverseTotal} | Power {k} | Gametick {l} | Y {rangeReverseTotalY} | Reverse {bestReverse}, {bestDiff} | Block {abs(rangeReverseTotal - projReverse)}\n")

if axis == "z":
    calcRatio(sandEfficiencyZ, reverseEfficiencyZ, sandZ, reverseZ)
else:
    calcRatio(sandEfficiencyX, reverseEfficiencyX, sandX, reverseX)

import json
from src.py.midairTools import barrelCalc, airDrag, gravity, headBlock

with open("src/py/midairLefty/decimalPosition.json", "r") as f:
    decimalPosition = json.load(f)

log = open("src/py/midairLefty/resultats.txt", "w", encoding="utf-8")

for blockNameSandX, offsetSandX in decimalPosition["north"].items():
    print(f"==== {blockNameSandX} ====\n")
    for blockNameLeftyX, offsetLeftyX in decimalPosition["north"].items():
        for blockNameLeftyDecal, offsetLeftyDecal in decimalPosition["north"].items():
            for prout in range(4,1, -1):
                for blockNameSandY, offsetSandY in decimalPosition["top"].items():
                    # Change parameters here
                    powerSandX, powerSandY, powerSandZ = 368248.50999999046, 6.0, -396648.50999999046
                    powerLeftyX, powerLeftyY, powerLeftyZ = 368248.50999999046, 6.0, -396648.50999999046
                    sandY, sandZ = 6.519999980926514, -396649.49000000954
                    leftyY, leftyZ = 7.519999980926514, -396650.49000000954

                    sandX = 368248 + offsetSandX
                    leftyX = 368248 + offsetLeftyX

                    leftyDecal = 368244 + offsetLeftyDecal
                    sandDecal = 368244.49000000954

                    tntAmount = 450
                    gametickMax = 14

                    diffGametick = prout

                    heightAdjustSandY = 40 + offsetSandY
                    heightAdjustLeftyY = 41.019999980926514

                    limitPower = 1000
                    errorVel = 0.001
                    errorVelY = 0.2

                    sandEfficiencyX, sandEfficiencyY, sandEfficiencyZ, sandDistanceEfficiency = barrelCalc(powerSandX, powerSandY, powerSandZ, sandX, sandY, sandZ)
                    leftyEfficiencyX, leftyEfficiencyY, leftyEfficiencyZ, leftyDistanceEfficiency = barrelCalc(powerLeftyX, powerLeftyY, powerLeftyZ, leftyX, leftyY, leftyZ)

                    def calcRatio(sandEfficiency, leftyEfficiency, projSand, projLefty, leftyDecal, sandDecal):
                        for i in range(200, tntAmount):
                            rangeSandValue = sandEfficiency * sandDistanceEfficiency * i
                            rangeSandTotal = rangeSandValue + projSand

                            rangeSandValueY = 0.0
                            rangeSandTotalY = heightAdjustSandY 

                            for j in range(2, gametickMax):
                                rangeSandValue *= airDrag
                                rangeSandTotal += rangeSandValue
                                velocity = rangeSandValue * airDrag

                                rangeSandValueY -= gravity
                                rangeSandTotalY += rangeSandValueY
                                rangeSandValueY *= airDrag

                                if 0.4 <= rangeSandTotal % 1 <= 0.6:

                                    for k in range(1, i):
                                        rangeLeftyValue = leftyEfficiency * leftyDistanceEfficiency * k
                                        rangeLeftyTotal = rangeLeftyValue + projLefty

                                        rangeLeftyValueY = 0.0
                                        rangeLeftyTotalY = heightAdjustLeftyY

                                        for l in range(2, j + diffGametick+1):
                                            rangeLeftyValue *= airDrag
                                            rangeLeftyTotal += rangeLeftyValue

                                            rangeLeftyValueY -= gravity
                                            rangeLeftyTotalY += rangeLeftyValueY
                                            rangeLeftyValueY *= airDrag


                                        if sandEfficiency > 0:
                                            behind = rangeLeftyTotal - rangeSandTotal
                                        else:
                                            behind = rangeSandTotal - rangeLeftyTotal

                                        if 0 <= behind <= 4 and j > 2:
                                            ratioLeftyEfficiencyX, ratioLeftyEfficiencyY, ratioLeftyEfficiencyZ, ratioLeftyDistanceEfficiency = barrelCalc(leftyDecal, rangeLeftyTotalY, rangeLeftyTotal, sandDecal, rangeSandTotalY, rangeSandTotal)

                                            bestLefty = None
                                            bestLeftyDiff = float('inf')

                                            for m in range(limitPower):
                                                velocityLefty = ratioLeftyEfficiencyZ * ratioLeftyDistanceEfficiency * m

                                                velocityFinal = velocity + velocityLefty

                                                diff = abs(velocityFinal)

                                                if diff < bestLeftyDiff:
                                                    bestLeftyDiff = diff
                                                    bestLefty = m

                                            velocitySandY = ratioLeftyEfficiencyY * ratioLeftyDistanceEfficiency * bestLefty
                                            velocityFinalY = rangeSandTotalY + velocitySandY + rangeSandValueY

                                            if bestLeftyDiff <= errorVel and (velocityFinalY - rangeLeftyTotalY) <= errorVelY and (velocityFinalY - rangeLeftyTotalY) >= -errorVelY:
                                                log.write(f"Sand Block {blockNameSandX} | Lefty Block {blockNameLeftyX} | Lefty Decal {blockNameLeftyDecal} | prout {prout} | sand y block {blockNameSandY}\n")
                                                log.write(f"Power {i} | Position {rangeSandTotal} | Distance {rangeSandTotal - projSand} | Gametick {j} | Velocity {velocity} | Position Y {rangeSandTotalY}\n")
                                                log.write(f"Power {k} | Lefty Amount {bestLefty} | Position {rangeLeftyTotal} | Position Y {rangeLeftyTotalY} | velo {velocityFinalY - rangeLeftyTotalY} | kaka {bestLeftyDiff}\n\n")
                                    
                    calcRatio(sandEfficiencyZ, leftyEfficiencyZ, sandZ, leftyZ, leftyDecal, sandDecal)
log.close()



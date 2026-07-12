from src.midairTools import barrelCalc, airDrag, gravity, headBlock

# Change parameters here
powerSandX, powerSandY, powerSandZ = 367911.49000000954, 17.0, -396863.50999999046
powerHammerX, powerHammerY, powerHammerZ = 367911.49000000954, 17.0, -396863.50999999046
sandX, sandY, sandZ = 367910.49000000954, 18.019999980926514, -396864.50999999046
hammerX, hammerY, hammerZ = 367910.49000000954, 18.019999980926514, -396864.50999999046

heightAdjustY = 254 + headBlock

tntAmount = 400
gametickMax = 24

diffGametick = 4

axis = "z"

limitPower = 1000

sandEfficiencyX, sandEfficiencyY, sandEfficiencyZ, sandDistanceEfficiency = barrelCalc(powerSandX, powerSandY, powerSandZ, sandX, sandY, sandZ)
hammerEfficiencyX, hammerEfficiencyY, hammerEfficiencyZ, hammerDistanceEfficiency = barrelCalc(powerHammerX, powerHammerY, powerHammerZ, hammerX, hammerY, hammerZ)

def calcRatio(sandEfficiency, hammerEfficiency, projSand, projHammer):
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

            if 0.49 <= rangeSandTotal % 1 <= 0.51:
                for k in range(i,limitPower):
                    rangeHammerValue = hammerEfficiency * hammerDistanceEfficiency * k
                    rangeHammerTotal = rangeHammerValue + projHammer

                    rangeHammerValueY = 0.0
                    rangeHammerTotalY = heightAdjustY

                    for l in range(1, j - diffGametick+1):
                        rangeHammerValue *= airDrag
                        rangeHammerTotal += rangeHammerValue

                        rangeHammerValueY -= gravity
                        rangeHammerTotalY += rangeHammerValueY
                        rangeHammerValueY *= airDrag

                    if sandEfficiency > 0:
                        behind = rangeHammerTotal - rangeSandTotal
                    else:
                        behind = rangeSandTotal - rangeHammerTotal

                    if 0 <= behind <= 4:
                        if axis == "z":
                            _, ratioHammerEfficiencyY, ratioHammerEfficiencyZ, ratioHammerDistanceEfficiency = barrelCalc(1, rangeHammerTotalY, rangeHammerTotal, 1, rangeSandTotalY, rangeSandTotal)
                        else:
                            ratioHammerEfficiencyX, ratioHammerEfficiencyY, _, ratioHammerDistanceEfficiency = barrelCalc(rangeHammerTotal, rangeHammerTotalY, 1, rangeSandTotal, rangeSandTotalY, 1)

                        bestHammer = None
                        bestDiff = float("inf")

                        for m in range(limitPower):
                            if axis == "z":
                                velocityHammer = ratioHammerEfficiencyZ * ratioHammerDistanceEfficiency *m
                            else:
                                velocityHammer = ratioHammerEfficiencyX * ratioHammerDistanceEfficiency *m

                            velocityFinal = velocity + velocityHammer

                            diff = abs(velocityFinal)

                            if diff < bestDiff:

                                bestDiff = diff
                                bestHammer = m

                        velocitySandY = ratioHammerEfficiencyY * ratioHammerDistanceEfficiency * bestHammer
                        velocityFinalY = rangeSandTotalY + velocitySandY + rangeSandValueY
                            
                        if velocityFinalY < 1:
                            print("SAND")
                            print(f"Power {i} | Position {rangeSandTotal} | Distance {rangeSandTotal - projSand} | Gametick {j} | Velocity {velocity} | Position Y {rangeSandTotalY}")
                            print("HAMMER")
                            print(f"Power {k} | Position {rangeHammerTotal} |  | Position Y {rangeHammerTotalY}")
                            print(f"Hammer {bestHammer} | velocity {bestDiff} | Y-velocity {velocityFinalY}\n")

if axis == "z":
    calcRatio(sandEfficiencyZ, hammerEfficiencyZ, sandZ, hammerZ)
else:
    calcRatio(sandEfficiencyX, hammerEfficiencyX, sandX, hammerX)
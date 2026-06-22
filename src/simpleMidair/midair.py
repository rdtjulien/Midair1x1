from src.midairTools import barrelCalc, airDrag, gravity, headBlock

powerSandX, powerSandY, powerSandZ = 368063.50999999046, 208.0, -396802.50999999046
powerHammerX, powerHammerY, powerHammerZ = 368063.50999999046, 208.0, -396802.50999999046
sandX, sandY, sandZ = 368064.00999999046, 208.5199999809265, -396801.49000000954
hammerX, hammerY, hammerZ = 368064.00999999046, 208.5199999809265, -396801.50999999046

heightAdjustY = 254 + headBlock

tntAmount = 1000
gametickMax = 16

diffGametick = 4

axis = "z"

limitPower = 5000

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

                    if 0 <= rangeHammerTotal - rangeSandTotal <= 4:
                        _, ratioHammerEfficiencyY, ratioHammerEfficiencyZ, ratioHammerDistanceEfficiency = barrelCalc(1, rangeHammerTotalY, rangeHammerTotal, 1, rangeSandTotalY, rangeSandTotal)

                        bestHammer = None
                        bestDiff = float("inf")

                        for m in range(limitPower):
                            velocityHammerZ = ratioHammerEfficiencyZ * ratioHammerDistanceEfficiency *m

                            velocityFinalZ = velocity + velocityHammerZ

                            diff = abs(velocityFinalZ)

                            if diff < bestDiff:
                                bestDiff = diff
                                bestHammer = m

                        velocitySandY = ratioHammerEfficiencyY * ratioHammerDistanceEfficiency * bestHammer
                        velocityFinalY = rangeSandTotalY + velocitySandY + rangeSandValueY
                            
                        if velocityFinalY < 1:
                            print("SAND")
                            print(f"Power {i} | Position {rangeSandTotal} | Distance {rangeSandTotal - projSand} | Gametick {j} | Velocity {velocity} | Position Y {rangeSandTotalY}")
                            print("HAMMER")
                            print(f"Power {k} | Position {rangeHammerTotal} | Gametick {l} | Position Y {rangeHammerTotalY}")
                            print(f"Hammer ~{bestHammer} | velocity {bestDiff} | Y-velocity {velocityFinalY}\n")

if axis == "z":
    calcRatio(sandEfficiencyZ, hammerEfficiencyZ, sandZ, hammerZ)
else:
    calcRatio(sandEfficiencyX, hammerEfficiencyX, sandX, hammerX)
from src.midairTools import barrelCalc, airDrag, gravity, headBlock

powerSandX, powerSandY, powerSandZ = 368006.5, 5.0, -396813.49000000954
powerHammerX, powerHammerY, powerHammerZ = 368006.5, 5.0, -396813.49000000954
sandX, sandY, sandZ = 368007.00999999046, 5.519999980926514, -396812.50999999046
hammerX, hammerY, hammerZ = 368007.00999999046, 5.519999980926514, -396812.50999999046

heightAdjustY = 11 + headBlock

tntAmount = 200
gametickMax = 10

diffGametick = 2

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
            rangeSandValueY *= airDrag
            rangeSandTotalY += rangeSandValueY

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
                        rangeHammerValueY *= airDrag
                        rangeHammerTotalY += rangeHammerValueY

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
                            print(f"Power {i} | Position {rangeSandTotal} | Distance {abs(rangeSandTotal - rangeSandValue)} | Gametick {j} | Velocity {velocity}")
                            print(f"Power {i} | Position {rangeSandTotalY} | Gametick {j}")
                            print("HAMMER")
                            print(f"Power {k} | Position {rangeHammerTotal} | Distance {abs(rangeHammerTotal - rangeHammerValue)} | Gametick {l}")
                            print(f"Power {k} | Position {rangeHammerTotalY} | Gametick {l}")
                            print(f"Hammer {bestHammer} | velocity {bestDiff} | Y-velocity {velocityFinalY}\n")

if axis == "z":
    calcRatio(sandEfficiencyZ, hammerEfficiencyZ, sandZ, hammerZ)
else:
    calcRatio(sandEfficiencyX, hammerEfficiencyX, sandX, hammerX)
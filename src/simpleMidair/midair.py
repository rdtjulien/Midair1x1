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
    for i in range(1):
        rangeSandValue = sandEfficiency * sandDistanceEfficiency * 110
        rangeSandTotal = rangeSandValue + projSand

        rangeSandValueY = 0.0
        rangeSandTotalY = heightAdjustY 

        for j in range(2, gametickMax):
            rangeSandValue *= airDrag
            rangeSandTotal += rangeSandValue

            rangeSandValueY -= gravity
            rangeSandValueY *= airDrag
            rangeSandTotalY += rangeSandValueY

            if 0.49 <= rangeSandTotal % 1 <= 0.51:
                print("SAND")
                print(f"Power {i} | Position {rangeSandTotal} | Distance {abs(rangeSandTotal - rangeSandValue)} | Gametick {j}")
                print(f"Power {i} | Position {rangeSandTotalY} | Gametick {j}\n")
                for k in range(110,limitPower):
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

                    if rangeHammerTotal >= rangeSandTotal -3 and rangeHammerTotal <= rangeSandTotal +3:
                        print("HAMMER")
                        print(f"Power {k} | Position {rangeHammerTotal} | Distance {abs(rangeHammerTotal - rangeHammerValue)} | Gametick {l}")
                        print(f"Power {k} | Position {rangeHammerTotalY} | Gametick {l}\n")
                        

if axis == "z":
    calcRatio(sandEfficiencyZ, hammerEfficiencyZ, sandZ, hammerZ)
else:
    calcRatio(sandEfficiencyX, hammerEfficiencyX, sandX, hammerX)
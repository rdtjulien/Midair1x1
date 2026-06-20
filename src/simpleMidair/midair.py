from src.midairTools import barrelCalc, airDrag

"""
calculate an 1x1 ratio
"""

def calcRatio(distanceEfficiency, efficiency, proj, gametickMax, tntAmount):
    for i in range(tntAmount):
        rangeValue = efficiency * distanceEfficiency * i
        rangeTotal = rangeValue + proj

        for j in range(2, gametickMax):
            rangeValue *= airDrag
            rangeTotal += rangeValue

            if 0.49 <= rangeTotal % 1 <= 0.51:
                print(f"Power {i} | Position {rangeTotal} | Distance {abs(rangeTotal - proj):.0f} | Gametick {j}")

# Change parameters here
powerX, powerY, powerZ = 368006.5, 5.0, -396813.49000000954
projX, projY, projZ = 368007.00999999046, 5.519999980926514, -396812.50999999046

tntAmount = 200
gametickMax = 10

axis = "z"

efficiencyX, _, efficiencyZ, distanceEfficiency = barrelCalc(powerX, powerY, powerZ, projX, projY, projZ)

if axis == "z":
    calcRatio(distanceEfficiency, efficiencyZ, projZ, gametickMax, tntAmount)
else:
    calcRatio(distanceEfficiency, efficiencyX, projX, gametickMax, tntAmount)

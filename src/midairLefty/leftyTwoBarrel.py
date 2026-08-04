import json
from src.midairTools import barrelCalc, airDrag, gravity, headBlock

with open("src/decimalPosition.json", "r") as f:
    decimalPosition = json.load(f)

# Change parameters here
powerSandX, powerSandY, powerSandZ = 368178.50999999046, 206.0, -396680.50999999046
sandX, sandY, sandZ = 368177.99000000954, 206.5199999809265, -396681.49000000954

leftyDecal = 368161
sandDecal = 368161.49000000954

tntAmount = 450
gametickMax = 10

axis = "z"

limitPower = 1000
errorVel = 0.001

#For json
direction = "north"

sandEfficiencyX, sandEfficiencyY, sandEfficiencyZ, sandDistanceEfficiency = barrelCalc(powerSandX, powerSandY, powerSandZ, sandX, sandY, sandZ)

def calcRatio(sandEfficiency, projSand, leftyDecal):
    for i in range(tntAmount):
        rangeSandValue = sandEfficiency * sandDistanceEfficiency * i
        rangeSandTotal = rangeSandValue + projSand

        for j in range(2, gametickMax):
            rangeSandValue *= airDrag
            rangeSandTotal += rangeSandValue
            velocity = rangeSandValue * airDrag


            if 0.49 <= rangeSandTotal % 1 <= 0.51:
                leftyZ = rangeSandTotal + (1 if velocity > 0 else -1)

                ratioLeftyX, _, ratioLeftyZ, ratioLeftyDistanceEfficiency = barrelCalc(leftyDecal, 1, leftyZ, sandDecal, 1, rangeSandTotal)

                bestLefty = None
                bestLeftyDiff = float('inf')

                for k in range(1, limitPower):
                    if axis == "x":
                        velocityLefty = ratioLeftyX * ratioLeftyDistanceEfficiency * k
                    else:
                        velocityLefty = ratioLeftyZ * ratioLeftyDistanceEfficiency * k

                    velocityFinal = velocity + velocityLefty

                    diff = abs(velocityFinal)

                    if diff < bestLeftyDiff:
                        bestLeftyDiff = diff
                        bestLefty = k

                if bestLeftyDiff <= errorVel:
                    print(f"Power {i} | Position {rangeSandTotal} | Distance {rangeSandTotal - projSand} | Gametick {j} | Velocity {velocity}")
                    print(f"Lefty amount: {bestLefty} vel {bestLeftyDiff}\n")

for blockName, offset in decimalPosition[direction].items():
    print(f"=== {blockName} ===")
    if axis == "z":
        calcRatio(sandEfficiencyZ, sandZ, leftyDecal + offset)
    else:
        calcRatio(sandEfficiencyX, sandX, leftyDecal + offset)


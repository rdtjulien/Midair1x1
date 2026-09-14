import json
from src.py.midairToolsLefty import barrelCalc
from src.py.midairCore import calcRatioCore
nbre = 0
with open("src/py/midairLefty/decimalPosition.json", "r") as f:
    decimalPosition = json.load(f)

log = open("src/py/midairLefty/resultats.txt", "w", encoding="utf-8")

for blockNameSandX, offsetSandX in decimalPosition["north"].items():
    print(f"==== {blockNameSandX} ====\n")
    for blockNameLeftyX, offsetLeftyX in decimalPosition["north"].items():
        for blockNameLeftyDecal, offsetLeftyDecal in decimalPosition["north"].items():
            for prout in range(4, 1, -1):
                for blockNameSandY, offsetSandY in decimalPosition["top"].items():
                    for blockNameSandDecal, offsetSandDecal in decimalPosition["north"].items():
                        for blockNameLeftyY, offsetLeftyY in decimalPosition["top"].items():
                            nbre += 1
                            powerSandX, powerSandY, powerSandZ = 368248.49000000954, 6.0, -396648.50999999046
                            powerLeftyX, powerLeftyY, powerLeftyZ = 368248.49000000954, 6.0, -396648.50999999046
                            sandY, sandZ = 6.519999980926514, -396649.49000000954
                            leftyY, leftyZ = 7.519999980926514, -396650.49000000954

                            sandX = 368248 + offsetSandX
                            leftyX = 368248 + offsetLeftyX

                            leftyDecal = 368244 + offsetLeftyDecal
                            sandDecal = 368244 + offsetSandDecal

                            if sandDecal < leftyDecal:
                                continue

                            tntAmount = 450
                            gametickMax = 14

                            diffGametick = prout

                            heightAdjustSandY = 40 + offsetSandY
                            heightAdjustLeftyY = 40 + offsetLeftyY

                            if heightAdjustSandY > heightAdjustLeftyY:
                                continue

                            limitPower = 1000
                            errorVel = 0.001
                            errorVelY = 0.1

                            sandEfficiencyX, sandEfficiencyY, sandEfficiencyZ, sandDistanceEfficiency = barrelCalc(
                                powerSandX, powerSandY, powerSandZ, sandX, sandY, sandZ)
                            leftyEfficiencyX, leftyEfficiencyY, leftyEfficiencyZ, leftyDistanceEfficiency = barrelCalc(
                                powerLeftyX, powerLeftyY, powerLeftyZ, leftyX, leftyY, leftyZ)

                            results = calcRatioCore(
                                sandEfficiencyZ, leftyEfficiencyZ, sandZ, leftyZ,
                                leftyDecal, sandDecal,
                                sandDistanceEfficiency, leftyDistanceEfficiency,
                                tntAmount, gametickMax, diffGametick,
                                heightAdjustSandY, heightAdjustLeftyY,
                                limitPower, errorVel, errorVelY
                            )

                            for row in results:
                                i, rangeSandTotal, distance, j, velocity, rangeSandTotalY, \
                                    k, bestLefty, rangeLeftyTotal, rangeLeftyTotalY, veloY, bestLeftyDiff = row

                                log.write(f"Sand Block {blockNameSandX} | Lefty Block {blockNameLeftyX} | sand decal {blockNameSandDecal} |"
                                        f"Lefty Decal {blockNameLeftyDecal} | prout {prout} | sand y block {blockNameSandY} | lefty y block {blockNameLeftyY}\n")
                                log.write(f"Power {int(i)} | Position {rangeSandTotal} | Distance {distance} | "
                                        f"Gametick {int(j)} | Velocity {velocity} | Position Y {rangeSandTotalY}\n")
                                log.write(f"Power {int(k)} | Lefty Amount {int(bestLefty)} | Position {rangeLeftyTotal} | "
                                        f"Position Y {rangeLeftyTotalY} | velo {veloY} | kaka {bestLeftyDiff}\n\n")

log.close()
print(f"Total iterations: {nbre}")
import numpy as np
from numba import njit
from src.py.midairToolsLefty import barrelCalc, airDrag, gravity

MAX_RESULTS = 20000

@njit(cache=True, fastmath=True)
def calcRatioCore(sandEfficiency, leftyEfficiency, projSand, projLefty,
                   leftyDecal, sandDecal,
                   sandDistanceEfficiency, leftyDistanceEfficiency,
                   tntAmount, gametickMax, diffGametick,
                   heightAdjustSandY, heightAdjustLeftyY,
                   limitPower, errorVel, errorVelY):

    results = np.empty((MAX_RESULTS, 12), dtype=np.float64)
    count = 0

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

            frac = rangeSandTotal % 1.0
            if 0.49 <= frac <= 0.51:

                for k in range(1, i):
                    rangeLeftyValue = leftyEfficiency * leftyDistanceEfficiency * k
                    rangeLeftyTotal = rangeLeftyValue + projLefty

                    rangeLeftyValueY = 0.0
                    rangeLeftyTotalY = heightAdjustLeftyY

                    for l in range(2, j + diffGametick + 1):
                        rangeLeftyValue *= airDrag
                        rangeLeftyTotal += rangeLeftyValue

                        rangeLeftyValueY -= gravity
                        rangeLeftyTotalY += rangeLeftyValueY
                        rangeLeftyValueY *= airDrag

                    if sandEfficiency > 0:
                        behind = rangeLeftyTotal - rangeSandTotal
                    else:
                        behind = rangeSandTotal - rangeLeftyTotal

                    if 0.0 <= behind <= 4.0 and j > 2:
                        ratioLeftyEfficiencyX, ratioLeftyEfficiencyY, ratioLeftyEfficiencyZ, ratioLeftyDistanceEfficiency = barrelCalc(leftyDecal, rangeLeftyTotalY, rangeLeftyTotal, sandDecal, rangeSandTotalY, rangeSandTotal)

                        bestLefty = 0
                        bestLeftyDiff = 1e18

                        for m in range(limitPower):
                            velocityLefty = ratioLeftyEfficiencyZ * ratioLeftyDistanceEfficiency * m
                            velocityFinal = velocity + velocityLefty
                            diff = abs(velocityFinal)
                            if diff < bestLeftyDiff:
                                bestLeftyDiff = diff
                                bestLefty = m

                        velocitySandY = ratioLeftyEfficiencyY * ratioLeftyDistanceEfficiency * bestLefty
                        velocityFinalY = rangeSandTotalY + velocitySandY + rangeSandValueY
                        veloY = velocityFinalY - rangeLeftyTotalY

                        if bestLeftyDiff <= errorVel and -errorVelY <= veloY <= errorVelY:
                            if count < MAX_RESULTS:
                                results[count, 0] = i
                                results[count, 1] = rangeSandTotal
                                results[count, 2] = rangeSandTotal - projSand
                                results[count, 3] = j
                                results[count, 4] = velocity
                                results[count, 5] = rangeSandTotalY
                                results[count, 6] = k
                                results[count, 7] = bestLefty
                                results[count, 8] = rangeLeftyTotal
                                results[count, 9] = rangeLeftyTotalY
                                results[count, 10] = veloY
                                results[count, 11] = bestLeftyDiff
                                count += 1

    return results[:count]
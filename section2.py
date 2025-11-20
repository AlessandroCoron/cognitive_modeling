from operator import pos
from drivermodel_python import *
import numpy as np
import math

import matplotlib.pyplot as plt


    
def plotTrial(locPos, locColor, trialTime, i=1):
    
    meanPos = sum(locPos)/len(locPos)
    maxPos = max(locPos)
    plt.figure(figsize=(20,6))  
    plt.scatter(range(len(locPos)), locPos, c=locColor, s=10)
    plt.xlabel("Time (in 50 ms steps)")
    plt.ylabel("Lateral position (m)")
    plt.figtext(.5, 0.95, f"Total trial time = {round(trialTime[0])} ms, Max lateral position = {round(maxPos, 2)} m, Mean lateral position = {round(meanPos, 2)} m", ha="center", fontsize=10)
    plt.title("Lateral position of vehicle over time")
    plt.subplots_adjust(left=0.04, right=0.98, top=0.9, bottom=0.10)
    plt.show()

    #plt.savefig(f"2B_{i}.png")

if __name__ == "__main__":
    #for i in range(1, 11):
        #locPos, locColor, trialTime = runTrial(interleaving="sentence", nrSentences=10, nrWordsPerSentence=17, nrSteeringMovementsWhenSteering=4)
        #plotTrial(locPos, locColor, trialTime, i)
    runSimulations2(nrSims=100)
    #locPos, locColor, trialTime = runTrialBonus(interleaving="sentence", nrSentences=2, nrWordsPerSentence=17, nrSteeringMovementsWhenSteering=4)
    #plotTrial(locPos, locColor, trialTime)
    #runTrialBonus(interleaving="word", nrSentences=1, nrWordsPerSentence=17, nrSteeringMovementsWhenSteering=4)

   



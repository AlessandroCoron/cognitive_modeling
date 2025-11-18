### 
### This code is developed by Christian P. Janssen of Utrecht University
### It is intended for students from the Master's course Cognitive Modeling
### Large parts are based on the following research papers:
### Janssen, C. P., & Brumby, D. P. (2010). Strategic adaptation to performance objectives in a dual‐task setting. Cognitive science, 34(8), 1548-1560. https://onlinelibrary.wiley.com/doi/full/10.1111/j.1551-6709.2010.01124.x
### Janssen, C. P., Brumby, D. P., & Garnett, R. (2012). Natural break points: The influence of priorities and cognitive and motor cues on dual-task interleaving. Journal of Cognitive Engineering and Decision Making, 6(1), 5-29. https://journals.sagepub.com/doi/abs/10.1177/1555343411432339
###
### If you want to use this code for anything outside of its intended purposes (training of AI students at Utrecht University), please contact the author:
### c.p.janssen@uu.nl



### 
### import packages
###

import random as rnd
import numpy
import math
import matplotlib.pyplot as plt
###
###
### Global parameters. These can be called within functions to change (Python: make sure to call GLOBAL)
###
###


###
### Car / driving related parameters
###
steeringUpdateTime = 250    #in ms ## How long does one steering update take? (250 ms consistent with Salvucci 2005 Cognitive Science)
timeStepPerDriftUpdate = 50 ### msec: what is the time interval between two updates of lateral position?
startingPositionInLane = 0.27 			#assume that car starts already slightly away from lane centre (in meters) (cf. Janssen & Brumby, 2010)


#parameters for deviations in car drift due the simulator environment: See Janssen & Brumby (2010) page 1555
gaussDeviateMean = 0
gaussDeviateSD = 0.13 ##in meter/sec



### The car is controlled using a steering wheel that has a maximum angle. Therefore, there is also a maximum to the lateral velocity coming from a steering update
maxLateralVelocity = 1.7	# in m/s: maximum lateral velocity: what is the maximum that you can steer?
minLateralVelocity = -1* maxLateralVelocity

startvelocity = 0 	#a global parameter used to store the lateral velocity of the car


###
### Switch related parameters
###
retrievalTimeWord = 200   #ms. ## How long does it take to think of the next word when interleaving after a word (time not spent driving, but drifting)
retrievalTimeSentence = 300 #ms. ## how long does it take to retrieve a sentence from memory (time not spent driving, but drifting)



###
### parameters for typing task
###
timePerWord = 0  ### ms ## How much time does one word take
wordsPerMinuteMean = 39.33   # parameters that control typing speed: when typing two fingers, on average you type this many words per minute. From Jiang et al. (2020; CHI)
wordsPerMinuteSD = 10.3 ## this si standard deviation (Jiang et al, 2020)


## Function to reset all parameters. Call this function at the start of each simulated trial. Make sure to reset GLOBAL parameters.
def resetParameters():
    global timePerWord
    global retrievalTimeWord
    global retrievalTimeSentence 
    global steeringUpdateTime 
    global startingPositionInLane 
    global gaussDeviateMean
    global gaussDeviateSD 
    global gaussDriveNoiseMean 
    global gaussDriveNoiseSD 
    global timeStepPerDriftUpdate 
    global maxLateralVelocity 
    global minLateralVelocity 
    global startvelocity
    global wordsPerMinuteMean
    global wordsPerMinuteSD
    
    timePerWord = 0 ### ms

    retrievalTimeWord = 200   #ms
    retrievalTimeSentence = 300 #ms
	
    steeringUpdateTime = 250    #in ms
    startingPositionInLane = 0.27 			#assume that car starts already away from lane centre (in meters)
	

    gaussDeviateMean = 0
    gaussDeviateSD = 0.13 ##in meter/sec
    gaussDriveNoiseMean = 0
    gaussDriveNoiseSD = 0.1	#in meter/sec
    timeStepPerDriftUpdate = 50 ### msec: what is the time interval between two updates of lateral position?
    maxLateralVelocity = 1.7	# in m/s: maximum lateral velocity: what is the maximum that you can steer?
    minLateralVelocity = -1* maxLateralVelocity
    startvelocity = 0 	#a global parameter used to store the lateral velocity of the car
    wordsPerMinuteMean = 39.33
    wordsPerMinuteSD = 10.3

	



##calculates if the car is not accelerating (m/s) more than it should (maxLateralVelocity) or less than it should (minLateralVelocity)  (done for a vector of numbers)
def velocityCheckForVectors(velocityVectors):
    global maxLateralVelocity
    global minLateralVelocity

    velocityVectorsLoc = velocityVectors

    if (type(velocityVectorsLoc) is list):
            ### this can be done faster with for example numpy functions
        velocityVectorsLoc = velocityVectors
        for i in range(len(velocityVectorsLoc)):
            if(velocityVectorsLoc[i]>1.7):
                velocityVectorsLoc[i] = 1.7
            elif (velocityVectorsLoc[i] < -1.7):
                velocityVectorsLoc[i] = -1.7
    else:
        if(velocityVectorsLoc > 1.7):
            velocityVectorsLoc = 1.7
        elif (velocityVectorsLoc < -1.7):
            velocityVectorsLoc = -1.7

    return velocityVectorsLoc  ### in m/s
	




## Function to determine lateral velocity (controlled with steering wheel) based on where car is currently positioned. See Janssen & Brumby (2010) for more detailed explanation.
## Lateral velocity update depends on current position in lane. Intuition behind function: the further away you are, the stronger the correction will be that a human makes
def vehicleUpdateActiveSteering(LD):

	latVel = 0.2617 * LD*LD + 0.0233 * LD - 0.022
	returnValue = velocityCheckForVectors(latVel)
	return returnValue ### in m/s
	
### function to update lateral deviation in cases where the driver is NOT steering actively (when they are distracted by typing for example). Draw a value from a random distribution. This can be added to the position where the car is already.
def vehicleUpdateNotSteering():
    
    global gaussDeviateMean
    global gaussDeviateSD

    

    vals = numpy.random.normal(loc=gaussDeviateMean, scale=gaussDeviateSD,size=1)[0]
    returnValue = velocityCheckForVectors(vals)
    return returnValue   ### in m/s

### Function to run a trial. Needs to be defined by students (section 2 and 3 of assignment)
def runTrial(nrWordsPerSentence =17, nrSentences=3, nrSteeringMovementsWhenSteering=2, interleaving="word"): 
    resetParameters()

    locPos = [startingPositionInLane]
    trialTime = 0   
    locColor = ["green"]

    if interleaving == "word":
        timePerWord =  60000/numpy.random.normal(loc=wordsPerMinuteMean, 
                                     scale=wordsPerMinuteSD, 
                                     size=1)
        for sentence in range(nrSentences):
            trialTime += retrievalTimeSentence
            locPos, locColor = updatePos(locPos, trialTime, retrievalTimeSentence, locColor)
            for word in range(nrWordsPerSentence):
                trialTime += timePerWord + retrievalTimeWord
                locPos, locColor = updatePos(locPos, trialTime, timePerWord + retrievalTimeWord, locColor)
                if not (sentence == nrSentences - 1 and word == nrWordsPerSentence - 1):
                    for i in range(nrSteeringMovementsWhenSteering):
                        startvelocity = vehicleUpdateActiveSteering(locPos[-1])
                        locPos, locColor = calculatePos(locPos, locColor, startvelocity, trialTime)
                        trialTime += steeringUpdateTime
    
    elif interleaving == "sentence":
        timePerWord =  60000/numpy.random.normal(loc=wordsPerMinuteMean, 
                                     scale=wordsPerMinuteSD, 
                                     size=1)
        for sentence in range(nrSentences):
            trialTime += retrievalTimeSentence
            
            locPos, locColor = updatePos(locPos, trialTime, retrievalTimeSentence, locColor)
            for word in range(nrWordsPerSentence):
                # print(timePerWord)
                trialTime += timePerWord
                locPos, locColor = updatePos(locPos, trialTime, timePerWord + retrievalTimeWord, locColor)
            if not (sentence == nrSentences - 1):
                for i in range(nrSteeringMovementsWhenSteering):
                    startvelocity = vehicleUpdateActiveSteering(locPos[-1])
                    locPos, locColor = calculatePos(locPos, locColor, startvelocity, trialTime)
                    trialTime += steeringUpdateTime
    elif interleaving == "none":
        timePerWord = 60000/ numpy.random.normal(loc=wordsPerMinuteMean, 
                                     scale=wordsPerMinuteSD, 
                                     size=1)
        for sentence in range(nrSentences):
            trialTime += retrievalTimeSentence
            locPos, locColor = updatePos(locPos, trialTime, retrievalTimeSentence, locColor)
            for word in range(nrWordsPerSentence):
                trialTime += timePerWord + retrievalTimeWord
                locPos, locColor = updatePos(locPos, trialTime, timePerWord + retrievalTimeWord, locColor)
                
    elif interleaving == "drivingOnly":
        timePerWord =  60000/ numpy.random.normal(loc=wordsPerMinuteMean, 
                                     scale=wordsPerMinuteSD, 
                                     size=1)
        for sentence in range(nrSentences):
            trialTime += retrievalTimeSentence
            for word in range(nrWordsPerSentence):
                trialTime += timePerWord + retrievalTimeWord
                if not (sentence == nrSentences - 1 and word == nrWordsPerSentence - 1):
                    for i in range(nrSteeringMovementsWhenSteering):
                        startvelocity = vehicleUpdateActiveSteering(locPos[-1])
                        locPos, locColor = calculatePos(locPos, locColor, startvelocity, trialTime)
                        trialTime += steeringUpdateTime
    
    return locPos, locColor, trialTime
    meanumpyos = sum(locPos)/len(locPos)
    maxPos = max(locPos)
    return round(trialTime[0]), maxPos, meanumpyos
                

                
def calculatePos(locPos, locColor, startvelocity, trialTime):
    for i in range(steeringUpdateTime//timeStepPerDriftUpdate):
        locPos.append(locPos[-1] -abs(startvelocity)*0.05)
        locColor.append("blue")
    return locPos, locColor

### function to run multiple simulations. Needs to be defined by students (section 3 of assignment)
def runSimulations(nrSims = 3):
    conditions = ["word", "sentence", "none", "drivingOnly"]
    totalTime = []
    meanDeviation = []
    maxDeviation = []
    Condition = []

    conditions = ["none", "drivingOnly", "word", "sentence"]
    symbols = {"none": "o", "drivingOnly": "^", "word": "x", "sentence": "s"}
    mean_colors = {"none": "blue", "drivingOnly": "red", "word": "green", "sentence": "black"}
    for condition in conditions:
        for sim in range(nrSims):
            trialTime, maxPos, meanumpyos = runTrial(interleaving=condition, nrSentences=10, nrWordsPerSentence= rnd.randint(15,20), nrSteeringMovementsWhenSteering=4)
            totalTime.append(trialTime)
            meanDeviation.append(meanumpyos)
            maxDeviation.append(maxPos)
            Condition.append(condition)
    plt.figure(figsize=(10, 6))

    for cond in conditions:

        # mask per condition
        mask = Condition == cond

        # raw datapoints (grey)
        plt.scatter(
            totalTime[mask],
            maxDeviation[mask],
            marker=symbols[cond],
            s=20,
            color="grey",
            label=f"{cond} (raw trials)" if cond == conditions[0] else None
        )

        # compute mean positions
        mean_time = numpy.mean(totalTime[mask])
        mean_maxDev = numpy.mean(maxDeviation[mask])
        std_time = numpy.std(totalTime[mask])
        std_maxDev = numpy.std(maxDeviation[mask])

        # mean marker (colored)
        plt.scatter(
            mean_time,
            mean_maxDev,
            marker=symbols[cond],
            color=mean_colors[cond],
            s=120,
            edgecolor="black",
            label=f"{cond} (mean)"
        )
        plt.xlim(min(totalTime) - 100, max(totalTime) + 100)
        plt.ylim(min(maxDeviation) - 0.1, max(maxDeviation) + 0.1)

        # error bars
        plt.errorbar(
            mean_time,
            mean_maxDev,
            xerr=std_time,
            yerr=std_maxDev,
            fmt=symbols[cond],
            color=mean_colors[cond],
            capsize=4
        )

    # Labels & legend
    plt.xlabel("Total Time (ms)")
    plt.ylabel("Max Lateral Deviation (m)")
    plt.title("Max Lateral Deviation vs Total Trial Time")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.autoscale(enable=True, axis='both', tight=False)

    plt.show()
    
def runSimulations2(nrSims = 3):
    conditions = ["word", "sentence", "none", "drivingOnly"]
    totalTime = []
    meanDeviation = []
    maxDeviation = []
    Condition = []

    for condition in conditions:
        for sim in range(nrSims):
            trialTime, maxPos, meanumpyos = runTrial(interleaving=condition, nrSentences=10, nrWordsPerSentence= rnd.randint(15,20), nrSteeringMovementsWhenSteering=4)
            totalTime.append(trialTime)
            meanDeviation.append(meanumpyos)
            maxDeviation.append(maxPos)
            Condition.append(condition)
    
    

    

def updatePos(locPos, trialTime, addedTime, locColor):
    totalTime = trialTime % 50
    totalTime += addedTime
    for i in range(math.floor(totalTime/50)):
        locPos.append(locPos[-1] + abs(vehicleUpdateNotSteering()*0.05))
        locColor.append("red")
    return locPos, locColor


def runSimulations2(nrSims = 3):
    conditions = ["word", "sentence", "none", "drivingOnly"]
    totalTime = []
    meanDeviation = []
    maxDeviation = []
    Condition = []

    conditions = ["none", "drivingOnly", "word", "sentence"]
    for condition in conditions:
        # 3. Iterate through the number of simulations
        for sim in range(nrSims):
            
            # Pick a random number from {15, 16, 17, 18, 19, 20}
            words_per_sentence = rnd.randint(15, 20)
            
            # Run the trial with specified parameters
            trialTime, maxPos, meanPos = runTrial(
                interleaving=condition,
                nrSentences=10,
                nrWordsPerSentence=words_per_sentence,
                nrSteeringMovementsWhenSteering=4
            )
            
            # Store the output in the four vectors
            totalTime.append(trialTime)
            meanDeviation.append(meanPos)
            maxDeviation.append(maxPos)
            Condition.append(condition)

    print("Simulations complete. Generating plot...")

    # --- Plotting Section ---
    
    # Convert lists to NumPy arrays for easier data manipulation
    totalTime = numpy.array(totalTime)
    maxDeviation = numpy.array(maxDeviation)
    Condition = numpy.array(Condition)
    
    # Create the figure
    plt.figure(figsize=(12, 8))
    
    # Define the unique styles for each condition
    # (marker, color, label)
    styles = {
        "word":        {"marker": "o", "color": "blue",  "label": "Word"},
        "sentence":    {"marker": "s", "color": "red",   "label": "Sentence"},
        "none":        {"marker": "x", "color": "green", "label": "None"},
        "drivingOnly": {"marker": "^", "color": "black", "label": "Driving Only"}
    }
    
    # We won't manually build this list; we'll let plt.legend() find the labels.
    # legend_handles = [] # To store handles for the legend

    for condition in conditions:
        # Get the style for this condition
        style = styles[condition]
        
        # Create a boolean "mask" to select data for *only* this condition
        mask = (Condition == condition)
        
        cond_times = totalTime[mask]
        cond_devs = maxDeviation[mask]
        
        # Plot the datapoints of individual trials
        # - Color is grey
        # - Symbol is unique (from 'style')
        # - alpha=0.4 makes them slightly transparent
        # - label='_nolegend_' hides these from the final legend
        plt.scatter(
            cond_times, 
            cond_devs, 
            color='grey', 
            marker=style["marker"], 
            alpha=0.4,
            label='_nolegend_'
        )

        # Calculate the average max lateral deviation and trial time
        mean_time = numpy.mean(cond_times)
        std_time = numpy.std(cond_times)
        
        mean_dev = numpy.mean(cond_devs)
        std_dev = numpy.std(cond_devs)

        # --- MODIFIED PLOTTING LOGIC ---
        
        # 1. Plot the error bars first.
        #    We use 'marker=None' so it *only* draws the bars,
        #    and 'label=_nolegend_' to hide it from the legend.
        plt.errorbar(
            x=mean_time,
            y=mean_dev,
            xerr=std_time,
            yerr=std_dev,
            marker='None',      # <-- No marker on the errorbar layer
            color=style["color"],
            capsize=5,        # Adds caps to the error bars
            linestyle='None', # Removes the connecting line
            label='_nolegend_', # <-- Hides from legend
            alpha=0.7           # Make bars slightly transparent
        )

        # 2. Plot the mean point *on top* using plt.scatter.
        #    This creates a clean marker for the legend.
        plt.scatter(
            x=mean_time,
            y=mean_dev,
            marker=style["marker"],
            color=style["color"],
            s=100,              # 's' is markersize squared (10*10)
            label=f'Mean: {style["label"]}', # <-- This label will be used
            zorder=5,           # Ensures markers are drawn on top
            edgecolors='black', # Adds a thin black outline
            linewidth=0.5
        )
        # We no longer need to append handles
        # legend_handles.append(handle)

    # Add plot titles and labels
    plt.title(f'Max Lateral Deviation vs Trial Time with ({nrSims} Sims per Condition)', fontsize=16)
    plt.xlabel('Trial Time in MS', fontsize=12)
    plt.ylabel('Max Lateral Deviation (meters)', fontsize=12)
    
    # Add the legend
    # plt.legend(handles=legend_handles, title="Condition Averages", fontsize=10)
    # A simple call to plt.legend() will now find the labeled scatter plots
    plt.legend(title="Condition Averages", fontsize=10)
    
    plt.grid(True, linestyle='--', alpha=0.6) # Add a faint grid
    plt.tight_layout() # Adjusts plot to prevent labels from overlapping
    
    # Show the plot
    plt.show()
    
    
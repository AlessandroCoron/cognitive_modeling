import matplotlib.pyplot as plt

def start(type = "middle"):
    if type == "middle":
        runtimeMS = 0
    elif type == "fast":
        runtimeMS = 0
    elif type == "slow":
        runtimeMS = 0
    return runtimeMS

def perceptualstep(type = "middle"):
    if type == "middle":
        runtimeMS = 100
    elif type == "fast":
        runtimeMS = 50
    elif type == "slow":
        runtimeMS = 200
    return runtimeMS

def cognitivestep(type = "middle"):
    if type == "middle":
        runtimeMS = 70
    elif type == "fast":
        runtimeMS = 25
    elif type == "slow":
        runtimeMS = 170
    return runtimeMS

def motorstep(type = "middle"):
    if type == "middle":
        runtimeMS = 70
    elif type == "fast":
        runtimeMS = 30
    elif type == "slow":
        runtimeMS = 100
    return runtimeMS

def example1():
    runtimeMSstart = start()
    runtimeMSperceptualstept = perceptualstep()
    runtimeMScognitivestep = cognitivestep()
    runtimeMSmotorstep = motorstep()
    return runtimeMSstart + runtimeMSperceptualstept + runtimeMScognitivestep + runtimeMSmotorstep

def extremes(type):
    runtimeMSstart = start(type)
    runtimeMSperceptualstept = perceptualstep(type)
    runtimeMScognitivestep = cognitivestep(type)
    runtimeMSmotorstep = motorstep(type)
    return runtimeMSstart + runtimeMSperceptualstept + runtimeMScognitivestep + runtimeMSmotorstep

def example2(completeness = "extremes"):
    total_time = []
    if completeness == "extremes":
        total_time.append(extremes("fast"))
        total_time.append(extremes("middle"))
        total_time.append(extremes("slow"))
    elif completeness == "all":
        conditions = ["middle", "fast", "slow"]
        
        for condition in conditions:
            for condition2 in conditions:
                for condition3 in conditions:
                    totaltime = perceptualstep(condition) + cognitivestep(condition2) + motorstep(condition3)
                    total_time.append(totaltime)
        plt.boxplot(total_time)
        plt.show()
    return total_time

def example3(tPtype = "middle", tCtype = "middle", tMtype = "middle"):
    totaltime = 0
    totaltime += perceptualstep(tPtype) * 2 + cognitivestep(tCtype) * 2 + motorstep(tMtype)
    return totaltime

def example3(tPtype = "middle", tCtype = "middle", tMtype = "middle"):
    totaltime = 0
    totaltime += perceptualstep(tPtype) * 2 + cognitivestep(tCtype) * 2 + motorstep(tMtype)
    return totaltime

def example4(tPtype = "middle", tCtype = "middle", tMtype = "middle"):
    timings = [40, 80, 110, 150, 210, 240]
    for timing in timings:
        totaltime = 0
        totaltime += perceptualstep(tPtype) 
        if timing > totaltime:
            totaltime = timing
        totaltime += perceptualstep(tPtype) + cognitivestep(tCtype) * 2 + motorstep(tMtype)
        print("Timing : " + str(timing) + " || Total time : " + str(totaltime))
    return totaltime

def example5():
    conditions = ["middle", "fast", "slow"]
    data = []
    for tPtype in conditions:
        for tCtype in conditions:
            for tMtype in conditions:
                error_probablility = 0.01
                if tPtype == "slow":
                    error_probablility *= 0.25 
                elif tPtype == "middle":
                    error_probablility *= 4
                elif tPtype == "fast":
                    error_probablility *= 9
                if tCtype == "slow":
                    error_probablility *= 0.25 
                elif tCtype == "middle":
                    error_probablility *= 4
                elif tCtype == "fast":
                    error_probablility *= 9
                if tMtype == "slow":
                    error_probablility *= 0.5
                elif tMtype == "middle":
                    error_probablility *= 2
                elif tMtype == "fast":
                    error_probablility *= 3

                totaltime = perceptualstep(tPtype) * 2 + cognitivestep(tCtype) * 2 + motorstep(tMtype)
                trial_time_error_probability = [totaltime, min(error_probablility*100, 100)]
                data.append(trial_time_error_probability)

    plt.scatter(x=[ x[0] for x in data], y = [y[1] for y in data] )
    plt.xlabel("Time (ms)")
    plt.ylabel("Error probability (%)")
    plt.show()

if __name__ == "__main__":
    # print(example1())
    # print(example2())
    # print(example2("all"))
    # print(example3("fast", "fast", "fast"))
    # print(example3("fast", "middle", "slow"))
    # example4("slow", "slow", "slow")
    example5()
    

    



    


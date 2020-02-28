import random
import copy
import statistics
from Utils import Utils
import simpy
import numpy as np
import plotly.graph_objects as go

interval = 1
randomSeeder = 40
ramMemory = 100
random.seed(randomSeeder)
processesToDoWithCpu = 3
cpuCapacity = 2
generateRandomInt = lambda: random.randint(1, 10)
generateNewSqueletons = lambda c: [{
    "id": _ + 1,
    "requiredRam": random.randint(1, 10),
    "numberOfInstructions": random.randint(1, 10),
    "timeElapsed": ""
} for _ in range(c)]
cpuTimeOut = 1


def new(env, process, container, myList):
    print("Here comer new process ", process["id"])
    with container.request() as request:
        yield request
        env.process(running(env, process, myList))


def running(env, process, myList):
    process["numberOfInstructions"] -= processesToDoWithCpu
    number = process["numberOfInstructions"]
    print("Processing request ", process["id"], " with pending ",  number if (number > 0) else number + processesToDoWithCpu)
    yield ramContainer.put(process["requiredRam"])
    yield env.timeout(cpuTimeOut)
    if 0 == number:
        process["timeElapsed"] = env.now - process["timeElapsed"]
        print("Liberando el proceso ", process["id"])

    elif 3 > number:
        process["numberOfInstructions"] = number + 3 if (number < 0) else number
        process["timeElapsed"] = env.now - process["timeElapsed"]
        print("Liberando anticipadamente el proceso ", process["id"], " con ",
              number if (number > 0) else number + processesToDoWithCpu, " pendientes tiempo ahorita ",  env.now)
    else:
        myList.append(process)



def processes(env, number, interval, container):
    myList = generateNewSqueletons(number)
    for process in myList:
        timeOut = random.expovariate(1.0 / interval)
        process["timeElapsed"] = process["timeElapsed"] if process["timeElapsed"] != "" else env.now
        print("Se ha creado el proceso ", process["id"], " tiempo ", env.now, "\nCon un tiemout: ", timeOut, "\n")
        yield env.timeout(timeOut)

        yield ramContainer.get(process["requiredRam"])
        env.process(new(env, process, container, myList))



    for i in myList:
        results[str(number)][i["id"]] = i


results = {"25":{}, "50":{}, "100": {}, "150": {}, "200":{}}
avgs = {"25":0, "50":0, "100": 0, "150": 0, "200": 0}
stdDeviation = {"25":0, "50":0, "100": 0, "150": 0, "200": 0}
standardDeviation = {"25":0, "50":0, "100": 0, "150": 0, "200": 0}
env = simpy.Environment()
# myList = generateNewSqueletons(25)
ramContainer = simpy.Container(env, init=100, capacity=100)
cpu = simpy.Resource(env, capacity=cpuCapacity)
env.process(processes(env, 25, interval, cpu))
env.process(processes(env, 50, interval, cpu))
env.process(processes(env, 100, interval, cpu))
env.process(processes(env, 150, interval, cpu))
env.process(processes(env, 200, interval, cpu))
env.run()



title = "Promedio y desviacion estandard por numero de procesos\nIntervalo " + str(interval) + "\nRam: " + str(ramMemory) \
        + "\nCapacidad de Cpu " + str(cpuCapacity) + " Instrucciones: " + str(processesToDoWithCpu)
for key, result in results.items():
    list = []
    for finish in result:
        avgs[key] += result[finish]["timeElapsed"]
        list.append(result[finish]["timeElapsed"])
    avgs[key] /= int(key)
    stdDeviation[key] = statistics.stdev(list)

print("Averages: ", avgs)
print("Desviacion Standard: ", stdDeviation)
labelsAvg={'x':'Promedio por numero de procesos', 'y':'Procesos'}
labels={'x':'Promedio por numero de procesos', 'y':'Procesos'}
fig = go.Figure()
fig.add_trace(go.Scatter(x=[x for x in avgs.values()], y=[25,50,100,150,200],
                    mode='lines+markers',
                    name='Promedio por numero de procesos'))
fig.add_trace(go.Scatter(x=[x for x in stdDeviation.values()], y=[25,50,100,150,200],
                    mode='lines+markers',
                    name='Desviacion estandar por numero de procesos')
              )
fig.update_layout(title=title, yaxis_title= "Numero de procesos")

fig.show()







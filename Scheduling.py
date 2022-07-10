from os import SCHED_RESET_ON_FORK
import random
from operator import itemgetter
from datetime import datetime
from sqlite3 import Cursor
from copy import deepcopy

# --------------------------
# ----create list of process with limited burs and arival time.
# --------------------------


def CreateProcesses(process, burstLimit, arivalLimit, priorityLimit):
    processList = []
    for i in range(process):
        proc = {}
        proc["processName"] = "p"+str(i)
        burst = random.randint(1, burstLimit)
        proc["burst"] = burst
        proc["priority"] = random.randint(1, priorityLimit)
        if i == 0:
            proc["arival"] = 0
        else:
            arival = random.randint(1, arivalLimit)
            proc["arival"] = arival
        processList.append(proc)
    return processList


# --------------------------
# ----implemention Fcfs algoritm on processList.
# --------------------------
def FCFS(processList):
    sortedProcessList = sorted(processList, key=itemgetter('arival'))
    listprocessinfo = []
    cursor = 0
    procesBurstTime = 0
    procesWaitingTime = 0
    for process in sortedProcessList:
        procesBurstTime += process["burst"]
        processinfo = {}
        if process["arival"] > cursor:
            processinfo["waitingTime"] = 0
            processinfo["processName"] = process["processName"]
            cursor = process["arival"]
            cursor += process["burst"]
            listprocessinfo.append(processinfo)
        else:
            processinfo["waitingTime"] = cursor - process["arival"]
            processinfo["processName"] = process["processName"]
            cursor += process["burst"]
            listprocessinfo.append(processinfo)
        procesWaitingTime += processinfo["waitingTime"]
    waitingTimeAvg = procesWaitingTime / len(listprocessinfo)
    cpuUtilization = int((procesBurstTime/cursor)*100)
    return listprocessinfo, cpuUtilization, waitingTimeAvg

# --------------------------
# ----implemention SJF algoritm on processList.
# --------------------------


def SJF(processList):
    sortedProcessList = sorted(processList, key=itemgetter('arival'))
    listprocessinfo = []
    cursor = 0
    size = len(sortedProcessList)
    # first arival process
    firstProcessinfo = {}
    firstProcessinfo["waitingTime"] = 0
    firstProcessinfo["processName"] = sortedProcessList[0]["processName"]
    cursor += sortedProcessList[0]["burst"]
    listprocessinfo.append(firstProcessinfo)
    sortedProcessList.remove(sortedProcessList[0])
    # -----------------------------------------------
    while(size != len(listprocessinfo)):
        sortedProcessList = sorted(sortedProcessList, key=itemgetter('burst'))
        n = 0
        while(n < len(sortedProcessList)):
            processinfo = {}
            if sortedProcessList[n]["arival"] <= cursor:
                processinfo["waitingTime"] = cursor - \
                    sortedProcessList[n]["arival"]
                processinfo["processName"] = sortedProcessList[n]["processName"]
                cursor += sortedProcessList[n]["burst"]
                listprocessinfo.append(processinfo)
                sortedProcessList.remove(sortedProcessList[n])
                n = 0
            else:
                n += 1
        if len(sortedProcessList) == 0:
            break
        # exeption arival process
        sortedProcessList = sorted(sortedProcessList, key=itemgetter('arival'))
        if sortedProcessList[0]["arival"] > cursor:
            exeptionProcessinfo = {}
            exeptionProcessinfo["waitingTime"] = 0
            exeptionProcessinfo["processName"] = sortedProcessList[0]["processName"]
            cursor = sortedProcessList[0]["arival"]
            cursor += sortedProcessList[0]["burst"]
            listprocessinfo.append(exeptionProcessinfo)
            sortedProcessList.remove(sortedProcessList[0])
        # -----------------------------------------------
    procesBurstTime = 0
    procesWaitingTime = 0
    for process in processList:
        procesBurstTime += process["burst"]
    for process in listprocessinfo:
        procesWaitingTime += process["waitingTime"]
    waitingTimeAvg = procesWaitingTime / len(listprocessinfo)
    cpuUtilization = int((procesBurstTime/cursor)*100)
    return listprocessinfo, cpuUtilization, waitingTimeAvg


# --------------------------
# ----implemention Priority algoritm scheduling on processList.
# --------------------------
def Priority(processList):
    sortedProcessList = sorted(processList, key=itemgetter('arival'))
    listprocessinfo = []
    cursor = 0
    size = len(sortedProcessList)
    # first arival process
    firstProcessinfo = {}
    firstProcessinfo["waitingTime"] = 0
    firstProcessinfo["processName"] = sortedProcessList[0]["processName"]
    cursor += sortedProcessList[0]["burst"]
    listprocessinfo.append(firstProcessinfo)
    sortedProcessList.remove(sortedProcessList[0])
    # -----------------------------------------------
    while(size != len(listprocessinfo)):
        sortedProcessList = sorted(
            sortedProcessList, key=itemgetter('priority'), reverse=True)
        n = 0
        while(n < len(sortedProcessList)):
            processinfo = {}
            if sortedProcessList[n]["arival"] <= cursor:
                processinfo["waitingTime"] = cursor - \
                    sortedProcessList[n]["arival"]
                processinfo["processName"] = sortedProcessList[n]["processName"]
                cursor += sortedProcessList[n]["burst"]
                listprocessinfo.append(processinfo)
                sortedProcessList.remove(sortedProcessList[n])
                n = 0
            else:
                n += 1
        if len(sortedProcessList) == 0:
            break
        # exeption arival process
        sortedProcessList = sorted(sortedProcessList, key=itemgetter('arival'))
        if sortedProcessList[0]["arival"] > cursor:
            exeptionProcessinfo = {}
            exeptionProcessinfo["waitingTime"] = 0
            exeptionProcessinfo["processName"] = sortedProcessList[0]["processName"]
            cursor = sortedProcessList[0]["arival"]
            cursor += sortedProcessList[0]["burst"]
            listprocessinfo.append(exeptionProcessinfo)
            sortedProcessList.remove(sortedProcessList[0])
        # -----------------------------------------------
    procesBurstTime = 0
    procesWaitingTime = 0
    for process in processList:
        procesBurstTime += process["burst"]
    for process in listprocessinfo:
        procesWaitingTime += process["waitingTime"]
    waitingTimeAvg = procesWaitingTime / len(listprocessinfo)
    cpuUtilization = int((procesBurstTime/cursor)*100)
    return listprocessinfo, cpuUtilization, waitingTimeAvg


def waitingTimeAVG(List):
    waitingTime = 0
    for process in List:
        waitingTime += process["startTime"] - process["arival"]
    return waitingTime / len(List)


# --------------------------
# ----implemention RoundRobin algoritm scheduling on processList.
# --------------------------
def RoundRobin(processList, quantom):
    sortedProcessList = sorted(processList, key=itemgetter('arival'))
    cursor = 0

    burstTime = 0
    for process in sortedProcessList:
        process["status"] = "not-complete"
        process["startTime"] = -1
        burstTime += process["burst"]

    while(True):

        for process in sortedProcessList:
            if (process["arival"] <= cursor) and (process["status"] == "not-complete" or process["status"] == "middle"):
                process["status"] = "middle"
                temp = 0
                if process["burst"] < quantom:
                    temp = process["burst"]
                process["burst"] -= quantom
                if process["startTime"] == -1:
                    process["startTime"] = cursor
                if temp == 0:
                    cursor += quantom
                else:
                    cursor += temp
                if process["burst"] <= 0:
                    process["status"] = "complete"

        numofCompleted = 0
        for process in sortedProcessList:
            if process["status"] == "complete":
                numofCompleted += 1
        if numofCompleted == len(sortedProcessList):
            break
        else:
            for process in sortedProcessList:
                if process["status"] == "middle":
                    break
                elif process["status"] == "not-complete":
                    cursor = process["arival"]
                    break
    wtAVG = waitingTimeAVG(sortedProcessList)
    cpuUtilize = int((burstTime/cursor)*100)
    return sortedProcessList, cpuUtilize, wtAVG


# --------------------------
# ----implemention SRT algoritm scheduling on processList.
# --------------------------
def SRT(processList):
    sortedProcessList = sorted(processList, key=itemgetter('arival'))
    cursor = 0
    ready = []
    completeList = []

    burstTime = 0
    for process in sortedProcessList:
        process["status"] = "not-complete"
        process["startTime"] = -1
        process["state"] = "sortedList"
        burstTime += process["burst"]
    while(True):

        for process in sortedProcessList:
            if process["arival"] <= cursor and process["state"] == "sortedList":
                process["state"] = "ready"
                ready.append(process)

        ready.sort(key=itemgetter('burst'))

        if len(completeList) >= len(processList):
            break

        if len(ready) == 0:
            temp = sortedProcessList
            temp = sorted(temp, key=itemgetter('arival'))
            for process in temp:
                if process["arival"] >= cursor and process["state"] == "sortedList":
                    process["state"] = "ready"
                    ready.append(process)
                    cursor = process["arival"]
                    break

        if ready[0]["status"] == "complete":
            completeList.append(ready[0])
            ready.remove(ready[0])
            continue
        elif ready[0]["status"] == "not-complete" and ready[0]["startTime"] == -1:
            ready[0]["startTime"] = cursor
        ready[0]["burst"] -= 1
        cursor += 1

        if ready[0]["burst"] <= 0:
            ready[0]["status"] = "complete"
            ready[0]["exitTime"] = cursor
    wtAVG = waitingTimeAVG(completeList)
    cpuUtilize = int((burstTime/cursor)*100)
    return completeList, wtAVG, cpuUtilize


def printTable(myDict, colList=None):
    if not colList:
        colList = list(myDict[0].keys() if myDict else [])
    myList = [colList]  # 1st row = header
    for item in myDict:
        myList.append([str(item[col] if item[col] is not None else '')
                      for col in colList])
    colSize = [max(map(len, col)) for col in zip(*myList)]
    formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
    myList.insert(1, ['-' * i for i in colSize])  # Seperating line
    for item in myList:
        print(formatStr.format(*item))


def Display():
    numberOfProcess = int(input("please enter nuber of Process: "))
    burstLimit = int(
        input("please enter time of burst limition for each process : "))
    arivalLimit = int(
        input("please enter time of arival limition for each process : "))
    priorityLimit = int(
        input("please enter priority limition for each process : "))
    quantom = int(input("please enter quantom for RoundRobin algoritm : "))
    list = CreateProcesses(numberOfProcess, burstLimit,
                           arivalLimit, priorityLimit)
    print("\n")
    printTable(list, colList=None)
    print("\n")
    while(True):
        menu_options = {
            1: 'FCFS algoritm.',
            2: 'SRT algoritm.',
            3: 'SJF algoritm.',
            4: 'RoundRobin algoritm.',
            5: 'Priority algoritm.',
            6: 'exit.',
        }
        for key in menu_options:
            print(key, "-", menu_options[key])
        option = int(input("Enter your choice: "))
        print("\n")
        if option == 1:
            P_FCFS = FCFS(deepcopy(list))
            printTable(P_FCFS[0], colList=None)
            print("\n")
            print("Cpu Utilization: " +
                  str(P_FCFS[1])+"      "+"waiting time avg: "+str(P_FCFS[2]))
            print("\n")
        elif option == 2:
            P_SRT = SRT(deepcopy(list))
            printTable(P_SRT[0], colList=None)
            print("\n")
            print("Cpu Utilization: " +
                  str(P_SRT[1])+"      "+"waiting time avg: "+str(P_SRT[2]))
            print("\n")
        elif option == 3:
            P_SJF = SJF(deepcopy(list))
            printTable(P_SJF[0], colList=None)
            print("\n")
            print("Cpu Utilization: " +
                  str(P_SJF[1])+"      "+"waiting time avg: "+str(P_SJF[2]))
            print("\n")
        elif option == 4:
            P_RoundRobin = RoundRobin(deepcopy(list), quantom)
            printTable(P_RoundRobin[0], colList=None)
            print("\n")
            print("Cpu Utilization: " +
                  str(P_RoundRobin[1])+"      "+"waiting time avg: "+str(P_RoundRobin[2]))
            print("\n")
        elif option == 5:
            P_Priority = Priority(deepcopy(list))
            printTable(P_Priority[0], colList=None)
            print("\n")
            print("Cpu Utilization: " +
                  str(P_Priority[1])+"      "+"waiting time avg: "+str(P_Priority[2]))
            print("\n")
        elif option == 6:
            break
        else:
            print("please enter a valid number.")
            print("\n")


Display()

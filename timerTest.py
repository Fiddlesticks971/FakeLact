from datetime import datetime
import time

MAXFLOW = 20
MAXDP = 6
STATICP = 50
RAMPTIME = 300000

saved_time = ((datetime.now().time().second + (60*datetime.now().time().minute))*100000) + datetime.now().time().microsecond

def getTime():
    new_time = ((datetime.now().time().second + (60*datetime.now().time().minute))*100000) + datetime.now().time().microsecond
    secs_passed = new_time - saved_time
    if secs_passed > RAMPTIME:
        flowrate = MAXFLOW
        diffP = MAXDP
        upstreamP = STATICP
        downstreamP = upstreamP - diffP
    elif secs_passed <= RAMPTIME:
        #add ramp values
        flowrate = MAXFLOW*(secs_passed/RAMPTIME)
        diffP = MAXDP*(secs_passed/RAMPTIME)
        upstreamP = STATICP
        downstreamP = upstreamP - diffP
    return [flowrate,diffP,upstreamP,downstreamP]

f=open("output.txt","w")
while saved_time + RAMPTIME >= ((datetime.now().time().second + (60*datetime.now().time().minute))*100000) + datetime.now().time().microsecond:
    values=getTime()
    f.write(str(values[0])+", "+str(values[1])+", "+str(values[2])+", "+str(values[3])+"\n")
f.close()




from pymodbus.server.async import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from twisted.internet.task import LoopingCall
import datetime

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

MAXFLOW = 20
MAXDP = 6
STATICP = 50
RAMPTIME = 3


saved_time = datetime.date(2000,1,1)

def RunLactMotor(a):
    log.debug("updating the context")
    context = a[0]
    register = 3
    slave_id = 0x00
    address = 0x1
    values = context[slave_id].getValues(register, address, count=1)
        
    if values[0] == 1:
        if saved_time == datetime.date(2000,1,1):
            saved_time = datetime.now().time()
        delta_time = datetime.now().time() - saved_time
        secs_passed = (delta_time.minutes * 60) + delta_time.seconds
        if secs_passed > RAMPTIME:
            flowrate = MAXFLOW
            diffP = MAXDP
            upstreamP = STATICP
            downstreamP = upstreamP - diffP
        elif secs_passed <= RAMPTIME:
            #add ramp values
            flowrate = MAXFLOW*(secs_passed/RAMPTIME)
            diffP = MAXDP*(secs_passed/RAMPTIME)
            upstreamP = STATICP*(secs_passed/RAMPTIME)
            downstreamP = upstreamP - diffP
    elif values[0] == 0:
        saved_time = datetime.date(2000,1,1)
        flowrate = 0
        diffP = 0
        upstreamP = STATICP
        downstreamP = STATICP

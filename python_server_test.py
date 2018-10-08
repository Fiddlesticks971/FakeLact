from pymodbus.server.async import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from twisted.internet.task import LoopingCall
import struct
import time

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

FLOWRATE = 25.5
INLETPRES = 50.12
DIFFPRESS = 12.0
OUTLETPRESS = 40.876
BSW = 3.0
FLOWRATE_REG = 0
INLETPRES_REG = 2
DIFFPRESS_REG = 4
OUTLETPRSS_REG = 6
BSW_REG = 8

def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])


def updater(a):
        log.debug("updating the context")
        context = a[0]
        register = 3
        slave_id = 0x00
        address = 0x10
        values = context[slave_id].getValues(register, address, count=10)
        flowRate = float_to_hex(FLOWRATE)
        inletPres = float_to_hex(INLETPRES)
        outletPress = float_to_hex(OUTLETPRESS)
        diffPress =float_to_hex(DIFFPRESS)
        bSW = float_to_hex(BSW)
        values[FLOWRATE_REG] =int('0x'+flowRate[2:6],16)
        values[FLOWRATE_REG+1] =int('0x'+flowRate[6:10],16)
        values[INLETPRES_REG] =int('0x'+inletPres[2:6],16)
        values[INLETPRES_REG+1] =int('0x'+inletPres[6:10],16)
        values[DIFFPRESS_REG] =int('0x'+diffPress[2:6],16)
        values[DIFFPRESS_REG+1] =int('0x'+diffPress[6:10],16)
        values[OUTLETPRSS_REG] =int('0x'+outletPress[2:6],16)
        values[OUTLETPRSS_REG+1] =int('0x'+outletPress[6:10],16)
        values[BSW_REG] =int('0x'+bSW [2:6],16)
        values[BSW_REG+1] =int('0x'+bSW [6:10],16)
        log.debug("new values: " + str(values))
        context[slave_id].setValues(register, address, values)

store = ModbusSlaveContext(di = ModbusSequentialDataBlock(0, [17]*100),
                        co = ModbusSequentialDataBlock(0, [17]*100),
                        hr = ModbusSequentialDataBlock(0, [17]*100),
                        ir = ModbusSequentialDataBlock(0, [17]*100))
context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName = 'Pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
identity.ProductName = 'Pymodbus Server'
identity.ModelName = 'Pymodbus Server'
identity.MajorMinorRevision = '1.0'

time = 5
# 5 seconds delay
loop = LoopingCall(f=updater, a=(context,))
loop.start(interval=5, now=False)
StartTcpServer(context, identity=identity, address=("localhost", 5020))

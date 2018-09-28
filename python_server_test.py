from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from twisted.internet.task import LoopingCall
import time

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

def updater(a):
    while True:
        log.debug("updating the context")
        context = a[0]
        register = 3
        slave_id = 0x00
        address = 0x10
        log.debug("here 1")
        values = context[slave_id].getValues(register, address, count=5)
        values = [v + 1 for v in values]
        log.debug("new values: " + str(values))
        context[slave_id].setValues(register, address, values)
        log.debug("here 2")
        time.sleep(3)

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
loop.start(interval=5, now=True)
StartTcpServer(context, identity=identity, address=("localhost", 5020))

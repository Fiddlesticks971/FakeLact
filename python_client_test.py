from pymodbus3.client.sync import ModbusTcpClient

client = ModbusTcpClient('127.0.0.1',5020)

regoutput = client.read_holding_registers(10,5)

for thing in regoutput.registers:
    print (thing)

client.close()

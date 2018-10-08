from pymodbus3.client.sync import ModbusTcpClient
import struct

def FloatConvert(num1,num2):
    str_output = '0x'+str(hex(num1))[2:6]+str(hex(num2))[2:6]+'000'
    return struct.unpack('<f',struct.pack('<I', int(str_output,16)))

client = ModbusTcpClient('127.0.0.1',5020)

regoutput = client.read_holding_registers(16,10)

print (FloatConvert(regoutput.registers[0],regoutput.registers[1]))
print (FloatConvert(regoutput.registers[2],regoutput.registers[3]))
print (FloatConvert(regoutput.registers[4],regoutput.registers[5]))
print (FloatConvert(regoutput.registers[6],regoutput.registers[7]))
print (FloatConvert(regoutput.registers[8],regoutput.registers[9]))

client.close()

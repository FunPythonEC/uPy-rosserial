"""
This is a script to prove
rosserial topic negotiation
and publish
"""

import machine as m
import uio
import struct
from time import sleep, sleep_ms, sleep_us

#rosserial protocol header
header=bytearray([0xff,0xfe])

#little-endian function
def le(h):
    h &= 0xffff
    return [h & 0xff, h >> 8]

#generic checksum
def checksum(arr):
    return 255-((sum(arr))%256)

#defined baudrate to use
baudrate=57600

#uart definition for tx2 and rx2
uart = m.UART(2,baudrate)
uart.init(baudrate, bits=8, parity=None, stop=1, txbuf=0)

#values for topic negotiation
topic_id=5
topic_name="Greet"
message_type="std_msgs/String"
md5sum='992ce8a1687cec8c8bd883ec73ca41d1'
buffer_size=30

#packet serialization for negotiation
packettopic=uio.StringIO()
def serialize(packet):
    packettopic.write(struct.pack('<H',topic_id))
    packettopic.write(struct.pack('<I%ss'%len(topic_name),len(topic_name),topic_name))
    packettopic.write(struct.pack('<I%ss'%len(message_type),len(message_type),message_type))
    packettopic.write(struct.pack('<I%ss'%len(md5sum),len(md5sum),md5sum))
    packettopic.write(struct.pack('<i',buffer_size))
serialize(packettopic)
packettopic=packettopic.getvalue().encode('utf-8')
packetlen=len(list(packettopic))
checksumlen=checksum([packetlen])
checksumpack=list([checksum(list([0,0]+list(packettopic)))])

#packet serialization for publishing
packetdata=uio.StringIO()
dato="hola funpython"
def serializeString(packet):
    packetdata.write(struct.pack('<I%ss'%len(dato),len(dato),dato))
serializeString(packetdata)
packetdata=packetdata.getvalue().encode('utf-8')
packetlendata=len(list(packetdata))
checksumlendata=checksum([packetlendata])
checksumpackdata=list([checksum(list([5,0]+list(packetdata)))])

listo=0

while True:
    data = uart.read()
    if data==b'\xff\xfe\x00\x00\xff\x00\x00\xff':
        #negotiation is made
        uart.write(header)
        uart.write(bytearray(le(packetlen)))
        uart.write(bytearray([checksumlen]))
        uart.write(bytearray([0,0]))
        uart.write(packettopic)
        uart.write(bytearray(checksumpack))
        print('enviado registro de topic')
        listo=1
    elif listo==1:
        #publishing to the node
        uart.write(header)
        uart.write(bytearray(le(packetlendata)))
        uart.write(bytearray([checksumlendata]))
        uart.write(bytearray([5,0]))
        uart.write(packetdata)
        uart.write(bytearray(checksumpackdata))
        print('enviado hola')
        sleep(1)      
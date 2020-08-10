"""
This is a script to prove
rosserial topic negotiation
and publish
"""

import machine as m
import uio
import struct
from time import sleep, sleep_ms, sleep_us

# rosserial protocol header
header = bytearray([0xFF, 0xFE])

# little-endian function
def le(h):
    h &= 0xFFFF
    return [h & 0xFF, h >> 8]


# generic checksum
def checksum(arr):
    return 255 - ((sum(arr)) % 256)


# defined baudrate to use
baudrate = 57600

# uart definition for tx2 and rx2
uart = m.UART(2, baudrate)
uart.init(baudrate, bits=8, parity=None, stop=1, txbuf=0)

# values for topic negotiation
topic_id = 1
topic_name = "chatter"
message_type = "std_msgs/String"
md5sum = "992ce8a1687cec8c8bd883ec73ca41d1"
buffer_size = 100

# packet serialization for negotiation
packettopic = uio.StringIO()


def serialize(packet):
    packettopic.write(struct.pack("<H", topic_id))
    packettopic.write(
        struct.pack("<I%ss" % len(topic_name), len(topic_name), topic_name)
    )
    packettopic.write(
        struct.pack("<I%ss" % len(message_type), len(message_type), message_type)
    )
    packettopic.write(struct.pack("<I%ss" % len(md5sum), len(md5sum), md5sum))
    packettopic.write(struct.pack("<i", buffer_size))


serialize(packettopic)
packettopic = packettopic.getvalue().encode("utf-8")
packetlen = len(list(packettopic))
checksumlen = checksum([packetlen])
checksumpack = list([checksum(list([1, 0] + list(packettopic)))])

listo = 0

while True:
    data = uart.read()
    if data == b"\xff\xfe\x00\x00\xff\x00\x00\xff":
        # negotiation is made
        uart.write(header)
        uart.write(bytearray(le(packetlen)))
        uart.write(bytearray([checksumlen]))
        uart.write(bytearray([1, 0]))
        uart.write(packettopic)
        uart.write(bytearray(checksumpack))
        print("enviado registro de topic")
        listo = 1
    elif listo == 1:
        data = uart.read()
        if data is not None:
            print(data[11:33])

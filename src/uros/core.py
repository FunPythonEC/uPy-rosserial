import machine as m
import uio
import struct
from time import sleep, sleep_ms, sleep_us
from rosserial_msgs._TopicInfo import TopicInfo

header=[0xff,0xfe]

class NodeHandle(object):
	def __init__(self, serial_id, baudrate):
		
		self.id=1

		self.advertised_topics=dict()
		self.serial_id=serial_id
		self.baudrate=baudrate
		self.uart = m.UART(self.serial_id, self.baudrate)
		self.uart.init(self.baudrate, bits=8, parity=None, stop=1, txbuf=0)

	def init_node(self):
		pass

	def _advertise_topic(self,topic_name, msg):

		register=TopicInfo()
		register.topic_id=self.id
		register.topic_name=topic_name
		register.message_type=msg._type
		register.md5sum=msg._md5sum

		self.advertised_topics[topic_name]=self.id

		self.id+=1

		try:
			register.buffer_size=msg.buffer_size
		except:
			pass

		#serialization
		packet=uio.StringIO()
		register.serialize(packet)

		packet=list(packet.getvalue().encode('utf-8'))
		length=len(packet)

		crclen=[checksum(le(length))]
		crcpack=[checksum([0,0]+packet)]

		#final packet to be sent
		fpacket=header+le(length)+crclen+[0,0]+packet+crcpack

		self.uart.write(bytearray(fpacket))



	def publish(self,topic_name,msg):
		if topic_name not in self.advertised_topics:
			self._advertise_topic(topic_name, msg)

		packet=uio.StringIO()
		msg.serialize(packet)

		packet=list(packet.getvalue().encode('utf-8'))
		length=len(packet)

		topic_id=le(self.advertised_topics.get(topic_name))
		crclen=[checksum(le(length))]
		crcpack=[checksum(topic_id+packet)]	

		fpacket=header+le(length)+crclen+topic_id+packet+crcpack
		self.uart.write(bytearray(fpacket))

	def subscribe(self):
		pass


def checksum(arr):
    return 255-((sum(arr))%256)

def le(h):
    h &= 0xffff
    return [h & 0xff, h >> 8]
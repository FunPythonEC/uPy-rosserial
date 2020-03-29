#libraries needed
#	machine: for uart usage
#	uio: packet buffer
#	struct: serlization
#	_TopicInfo: for topic negotiation

import machine as m
import uio
import ustruct as struct
from time import sleep, sleep_ms, sleep_us
from rosserial_msgs._TopicInfo import TopicInfo

#rosserial protocol header
header=[0xff,0xfe]

#class to manage publish and subscribe
#COULD BE CHANGED AFTERWARDS
class NodeHandle(object):
	def __init__(self, serial_id, baudrate):
		
		"""
		id: used for topics id (negotiation)
		advertised_topics: manage alreade negotiated topics
		serial_id: uart id
		baudrate: baudrate used for serial comm
		"""
		self.id=1
		self.advertised_topics=dict()
		self.serial_id=serial_id
		self.baudrate=baudrate
		self.uart = m.UART(self.serial_id, self.baudrate)
		self.uart.init(self.baudrate, bits=8, parity=None, stop=1, txbuf=0)


	#method to manage and advertise topic
	#before publishing or subscribing
	def _advertise_topic(self,topic_name, msg):

		"""
		topic_name: eg. (/std_msgs/Greet)
		msg: message object
		"""
		register=TopicInfo()
		register.topic_id=self.id
		register.topic_name=topic_name
		register.message_type=msg._type
		register.md5sum=msg._md5sum

		self.advertised_topics[topic_name]=self.id

		#id are summed by one
		self.id+=1

		try:
			register.buffer_size=msg.buffer_size
		except Exception as e:
			print(e)

		#serialization
		packet=uio.StringIO()
		register.serialize(packet)

		#already serialized (packet)
		packet=list(packet.getvalue().encode('utf-8'))
		length=len(packet)

		#both checksums
		crclen=[checksum(le(length))]
		crcpack=[checksum([0,0]+packet)]

		#final packet to be sent
		fpacket=header+le(length)+crclen+[0,0]+packet+crcpack
		self.uart.write(bytearray(fpacket))


	def publish(self,topic_name,msg):

		if topic_name not in self.advertised_topics:
			self._advertise_topic(topic_name, msg)

		#same as advertise
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

#checksum method, receives array
def checksum(arr):
    return 255-((sum(arr))%256)
#little-endian method
def le(h):
    h &= 0xffff
    return [h & 0xff, h >> 8]
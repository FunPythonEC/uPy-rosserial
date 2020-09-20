"""
libraries needed
	machine: for uart usage
	uio: packet buffer
	struct: serlization
	_TopicInfo: for topic negotiation
   already provided in rosserial_msgs
"""

import machine as m
import uio
import ustruct as struct
from time import sleep, sleep_ms, sleep_us
from rosserial_msgs import TopicInfo
import sys
import os
import logging

# for now threads are used, will be changed with asyncio in the future
if sys.platform == "esp32":
    import _thread as threading
else:
    import threading

# rosserial protocol header
header = [0xFF, 0xFE]

logging.basicConfig(level=logging.INFO)

# class to manage publish and subscribe
# COULD BE CHANGED AFTERWARDS
class NodeHandle(object):
    def __init__(self, serial_id=2, baudrate=115200, **kwargs):

        """
		id: used for topics id (negotiation)
		advertised_topics: manage already negotiated topics
		subscribing_topics: topics to which will be subscribed are here
		serial_id: uart id
		baudrate: baudrate used for serial comm
		"""
        self.id = 101
        self.advertised_topics = dict()
        self.subscribing_topics = dict()
        self.serial_id = serial_id
        self.baudrate = baudrate

        if "serial" in kwargs:
            self.uart = kwargs.get("serial")
        elif "tx" in kwargs and "rx" in kwargs:
            self.uart = m.UART(self.serial_id, self.baudrate)
            self.uart.init(
                self.baudrate,
                tx=kwargs.get("tx"),
                rx=kwargs.get("rx"),
                bits=8,
                parity=None,
                stop=1,
                txbuf=0,
            )
        else:
            self.uart = m.UART(self.serial_id, self.baudrate)
            self.uart.init(self.baudrate, bits=8, parity=None, stop=1, txbuf=0)

        if sys.platform == "esp32":
            threading.start_new_thread(self._listen, ())
        else:
            threading.Thread(target=self._listen).start()

    # method to manage and advertise topic
    # before publishing or subscribing
    def _advertise_topic(self, topic_name, msg, endpoint, buffer_size):

        """
		topic_name: eg. (Greet)
		msg: message object
		endpoint: corresponds to TopicInfo.msg typical topic id values
		"""
        register = TopicInfo()
        register.topic_id = self.id
        register.topic_name = topic_name
        register.message_type = msg._type
        register.md5sum = msg._md5sum

        self.advertised_topics[topic_name] = self.id

        # id are summed by one
        self.id += 1

        try:
            register.buffer_size = buffer_size
        except Exception as e:
            logging.info("No buffer size could be defined for topic negotiation.")

        # serialization
        packet = uio.StringIO()
        register.serialize(packet)

        # already serialized (packet)
        packet = list(packet.getvalue().encode("utf-8"))
        length = len(packet)

        # both checksums
        crclen = [checksum(le(length))]
        crcpack = [checksum(le(endpoint) + packet)]

        # final packet to be sent
        fpacket = header + le(length) + crclen + le(endpoint) + packet + crcpack
        self.uart.write(bytearray(fpacket))

    def publish(self, topic_name, msg, buffer_size=1024):

        if topic_name not in self.advertised_topics:
            self._advertise_topic(topic_name, msg, 0, buffer_size)

        # same as advertise
        packet = uio.StringIO()
        msg.serialize(packet)

        packet = list(packet.getvalue().encode("utf-8"))
        length = len(packet)

        topic_id = le(self.advertised_topics.get(topic_name))
        crclen = [checksum(le(length))]
        crcpack = [checksum(topic_id + packet)]

        fpacket = header + le(length) + crclen + topic_id + packet + crcpack
        self.uart.write(bytearray(fpacket))

    def subscribe(self, topic_name, msgobj, cb, buffer_size=1024):
        assert cb is not None, "Subscribe callback is not set"

        # subscribing topic attributes are added
        self.subscribing_topics[self.id] = [msgobj, cb]

        # advertised if not already subscribed
        if topic_name not in self.advertised_topics:
            msg = msgobj()
            self._advertise_topic(topic_name, msg, 1, buffer_size)

    def _listen(self):
        while True:
            try:
                flag = self.uart.read(2)
                # check header
                if flag == b"\xff\xfe":
                    # get bytes length
                    lengthbyte = self.uart.read(2)
                    length = word(list(lengthbyte)[0], list(lengthbyte)[1])
                    lenchk = self.uart.read(1)

                    # validate length checksum
                    lenchecksum = sum(list(lengthbyte)) + ord(lenchk)
                    if lenchecksum % 256 != 255:
                        raise ValueError("Length checksum is not right!")

                    topic_id = list(self.uart.read(2))
                    inid = word(topic_id[0], topic_id[1])
                    if inid != 0:
                        msgdata = self.uart.read(length)
                        chk = self.uart.read(1)

                        # validate topic plus msg checksum
                        datachecksum = sum((topic_id)) + sum(list(msgdata)) + ord(chk)
                        if datachecksum % 256 == 255:
                            try:
                                # incoming object msg initialized
                                msgobj = self.subscribing_topics.get(inid)[0]
                            except Exception:
                                logging.info("TX request was made or got message from not available subscribed topic.")
                            # object sent to callback
                            callback = self.subscribing_topics.get(inid)[1]
                            fdata = msgobj()
                            fdata = fdata.deserialize(msgdata)
                            callback(fdata)
                        else:
                            raise ValueError("Message plus Topic ID Checksum is wrong!")

            except Exception as e:
                logging.info("No incoming data could be read for subscribes.")


# functions to be used in class
def word(l, h):
    """
	Given a low and high bit, converts the number back into a word.
	"""
    return (h << 8) + l


# checksum method, receives array
def checksum(arr):
    return 255 - ((sum(arr)) % 256)


# little-endian method
def le(h):
    h &= 0xFFFF
    return [h & 0xFF, h >> 8]


# example code
if __name__ == "__main__":
    from std_msgs import String
    from uros import NodeHandle

    msg = String()
    msg.data = "HiItsMeMario"
    node = NodeHandle(2, 115200)
    while True:
        node.publish("greet", msg)

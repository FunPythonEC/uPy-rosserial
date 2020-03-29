import ustruct as struct

class TopicInfo(object):

	md5sum = "0ad51f88fc44892f8c10684077646005"
	_type = "rosserial_msgs/TopicInfo"
	_has_header = False #flag to mark the presence of a Header object
	_full_text = """# special topic_ids
uint16 ID_PUBLISHER=0
uint16 ID_SUBSCRIBER=1
uint16 ID_SERVICE_SERVER=2
uint16 ID_SERVICE_CLIENT=4
uint16 ID_PARAMETER_REQUEST=6
uint16 ID_LOG=7
uint16 ID_TIME=10
uint16 ID_TX_STOP=11

# The endpoint ID for this topic
uint16 topic_id

string topic_name
string message_type

# MD5 checksum for this message type
string md5sum

# size of the buffer message must fit in
int32 buffer_size
"""

	ID_PUBLISHER = 0
	ID_SUBSCRIBER = 1
	ID_SERVICE_SERVER = 2
	ID_SERVICE_CLIENT = 4
	ID_PARAMETER_REQUEST = 6
	ID_LOG = 7
	ID_TIME = 10
	ID_TX_STOP = 11

	def __init__(self):

		self.topic_id=0
		self.topic_name=''
		self.message_type=''
		self.md5sum=''
		self.buffer_size=0

	def serialize(self, buff):
		try:
			buff.write(struct.pack('<H',self.topic_id))
			buff.write(struct.pack('<I%ss'%len(self.topic_name),len(self.topic_name),self.topic_name))
			buff.write(struct.pack('<I%ss'%len(self.message_type),len(self.message_type),self.message_type))
			buff.write(struct.pack('<I%ss'%len(self.md5sum),len(self.md5sum),self.md5sum))
			buff.write(struct.pack('<i',self.buffer_size))
		except Exception as e:
			print(e)

	def deserialize(self, str):
		try:
			end=0
			start=end
			end+=2
			(self.topic_id,) = struct.unpack('<H', str[start:end])
			start = end
			end += 4
			(length,) = struct.unpack('<I', str[start:end])
			start = end
			end += length
			self.topic_name = str[start:end].decode('utf-8')
			start = end
			end += 4
			(length,) = struct.unpack('<I',str[start:end])
			start = end
			end += length
			self.message_type=str[start:end].decode('utf-8')
			start = end
			end += 4
			(length,) = struct.unpack('<I', str[start:end])
			start = end
			end += length
			self.md5sum = str[start:end].decode('utf-8')
			start = end
			end += 4
			(self.buffer_size,) = struct.unpack('<i',str[start:end])
			return self
		except Exception as e:
			print(e)

			



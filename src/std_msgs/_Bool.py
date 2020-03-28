import ustruct as struct

class Bool(object):
	_md5sum = "8b94c1b53db61fb6aed406028ad6332a"
	_type = "std_msgs/Bool"
	_has_header = False #flag to mark the presence of a Header object
	_full_text = """bool data"""
	__slots__ = ['data']
	_slot_types = ['bool']

	def __init__(self):
		self.data = None

	def serialize(self, buff):
		try:
			buff.write(struct.pack('<B', self.data))
		except Exception as e:
			print(e)

	def deserialize(self, str):
		try:
			end = 0
			start = end
			end += 1
			(self.data,) = struct.unpack('<B', str[start:end])
			self.data = bool(self.data)
			return self
		except Exception as e:
			print(e)
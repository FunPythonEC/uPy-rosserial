import ustruct as struct

class Int64(object):
	_md5sum = "34add168574510e6e17f5d23ecc077ef"
	_type = "std_msgs/Int64"
	_has_header = False #flag to mark the presence of a Header object
	_full_text = """int64 data"""

	def __init__(self):
		self.data=0

	def serialize(self, buff):
		try:
			buff.write(struct.pack('<q', self.data))
		except Exception as e:
			print(e)

	def deserialize(self, str):
		try:
			end = 0
			start = end
			end += 8
			(self.data,) = struct.unpack('<q', str[start:end])
			return self
		except Exception as e:
			print(e)

import struct as ustruct

class Byte(object):
	_md5sum = "ad736a2e8818154c487bb80fe42ce43b"
	_type = "std_msgs/Byte"
	_has_header = False #flag to mark the presence of a Header object
	_full_text = """byte data
"""

	def __init__(self):
		self.data=0

	def serialize(self, buff):
		try:
			buff.write(struct.pack('<b', self.data))
		except Exception as e:
			print(e)

	def deserialize(self, str):
		try:
			end = 0
			start = end
			end += 1
			(self.data,) = struct.unpack('<b', str[start:end])
			return self	
		except Exception as e:
			print(e)
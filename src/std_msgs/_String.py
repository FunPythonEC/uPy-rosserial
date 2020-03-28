import ustruct as struct

class String(object):
	_md5sum = "992ce8a1687cec8c8bd883ec73ca41d1"
	_type = "std_msgs/String"
	_has_header = False #flag to mark the presence of a Header object
	_full_text = """string data
"""

	def __init__(self):
		self.data=''

	def serialize(self, buff):
		try:
			buff.write(struct.pack('<I%ss'%len(self.data), len(self.data), self.data))
		except Exception as e:
			print(e)

	def deserialize(self,str):
		try:
			end = 0
			start = end
			end += 4
			(length,) = struct.unpack('<I', str[start:end])
			start = end
			end += length
			self.data = str[start:end].decode('utf-8')
			return self
		except Exception as e:
			print(e)



""" Module for building an image and writing png files,
	written using only the Python standard library.

	Example usage:
		image = Image(50, 50)
		image.setPixel(0, 49, Color(255, 0, 0, 255))
		image.saveAsPNG("redDot.png")
"""

import zlib, struct

class Color(object):
	""" A small class representing a 32-bit RGBA color."""
	def __init__(self, r, g, b, a):
		self.color = (r, g, b, a)

	def getTuple(self):
		return self.color

	def getHexString(self):
		return "0x%02X%02X%02X%02X" % self.color

	def getByteString(self):
		""" Pack the color as a C-style byte string."""
		return struct.pack('>4B', self.color[0], self.color[1], self.color[2], self.color[3])

class Image(object):
	""" An image class capable of generating and saving a PNG.
		Attributes:
			width: The width of the image
			height: The height of the image
			buffer: Representation of the image storing Color values for each pixel
	"""
	def __init__(self, width, height):
		""" Create the buffer, fill it with black pixels."""
		self.width = width
		self.height = height
		self.buffer = []
		for i in range(0, width * height):
			self.buffer.append(Color(0, 0, 0, 255))

	def setPixel(self, x, y, color):
		""" Set the color value for the pixel at (x, y)."""
		if (x not in range(0, self.width)) or (y not in range (0, self.height)):
			raise ValueError("Trying to set a pixel outside of the image bounds.")

		index = (self.height - y - 1) * self.width + x
		self.buffer[index] = color

	def saveAsPNG(self, filename = "render.png"):
		""" Pack a new buffer formatted as a PNG, then save it to a file."""
		print("Saving PNG...")

		# First, create a binary string containing the image's raw color data
		data = b''
		for i in range(0, self.width*self.height):
			# Append null bytes at the beginning of rows
			if (i % self.width == 0):
				data += b'\x00'

			data += self.buffer[i].getByteString()

		def makeChunk(chunkType, chunkData):
			""" Pack data into standard PNG chunks. Chunks consist of:
					- a 4-byte length 
					- a 4-byte chunk type 
					- the chunk data (compressed)
					- a 4-byte cyclic redundancy check value (CRC)
			"""
			chunk = struct.pack(">I", len(chunkData)) + \
					chunkType + \
					chunkData +	\
					struct.pack(">I", 0xFFFFFFFF & zlib.crc32(chunkType + chunkData))

			return chunk

		# Compose the PNG out of 3 chunks using the above function:
		#	- IHDR: Header containing image size, color depth, existence of alpha channel etc. (See PNG spec)
		#	- IDAT: Chunk containing the actual image data
		#	- IEND: End-of-image chunk

		# Start with the universal PNG signature identifying the file as a PNG, then append chunks
		packedData = b'\x89PNG\r\n\x1a\n' +	\
					 makeChunk(b'IHDR', struct.pack(">2I5B", self.width, self.height, 8, 6, 0, 0, 0)) + \
					 makeChunk(b'IDAT', zlib.compress(data, 9)) + \
					 makeChunk(b'IEND', b'')

		png = open(filename, 'wb')
		png.write(packedData)
		png.close()
		
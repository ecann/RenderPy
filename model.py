""" Module for reading a .obj file into a stored model,
	retrieving vertices, faces, properties of that model.
	Written using only the Python standard library.
"""

from vector import Vector

class Model(object):
	def __init__(self, file):
		self.vertices = []
		self.faces = []

		# Read in the file
		f = open(file, 'r')
		for line in f:
			if line.startswith('#'): continue
			segments = line.split()
			if not segments: continue

			# Vertices
			if segments[0] == 'v':
				vertex = Vector(*[float(i) for i in segments[1:4]])
				self.vertices.append(vertex)

			# Faces
			elif segments[0] == 'f':
				face = []
				for s in segments[1:]:
					coords = s.split('/')
					face.append(int(coords[0])-1)

				self.faces.append(face)

	def normalizeGeometry(self):
		maxCoords = [0, 0, 0]

		for vertex in self.vertices:
			maxCoords[0] = max(abs(vertex.x), maxCoords[0])
			maxCoords[1] = max(abs(vertex.y), maxCoords[1])
			maxCoords[2] = max(abs(vertex.z), maxCoords[2])

		for vertex in self.vertices:
			vertex.x = vertex.x / maxCoords[0]
			vertex.y = vertex.y / maxCoords[1]
			vertex.z = vertex.z / maxCoords[2]

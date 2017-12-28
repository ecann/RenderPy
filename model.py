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
				# Support models that have faces with more than 3 points
				# Parse the face as a triangle fan
				for i in range(2, len(segments)-1):
					corner1 = int(segments[1].split('/')[0])-1
					corner2 = int(segments[i].split('/')[0])-1
					corner3 = int(segments[i+1].split('/')[0])-1
					self.faces.append([corner1, corner2, corner3])

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

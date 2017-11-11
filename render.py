from image import Image, Color
from model import Model
from shape import Point, Line, Triangle
from vector import Vector

width = 500
height = 300
image = Image(width, height, Color(255, 255, 255, 255))

# Load the model
model = Model('data/cow.obj')
model.normalizeGeometry()

def getOrthographicProjection(x, y, z):
	# Convert vertex from world space to screen space
	# by dropping the z-coordinate (Orthographic projection)
	screenX = int((x+1.0)*width/2.0)
	screenY = int((y+1.0)*height/2.0)

	return screenX, screenY

for face in model.faces:
	p0, p1, p2 = [model.vertices[i] for i in face]

	# Calculate the normal vector of this face and use it to calculate simple shading
	# Shading intensity is the scalar product of the light vector and the normal to the face
	# (p2-p0) x (p1-p0)
	normal = (p2-p0).cross(p1-p0).normalize()


	lightDir = Vector(0, 0, -1)
	intensity = normal * lightDir

	# Intensity < 0 means light is shining through the back of the face
	# In this case, don't draw the face at all ("back-face culling")
	if intensity < 0:
		continue

	transformedPoints = []
	for p in [p0, p1, p2]:
		screenX, screenY = getOrthographicProjection(p.x, p.y, p.z)
		transformedPoints.append(Point(screenX, screenY, Color(intensity*255, intensity*255, intensity*255, 255)))

	Triangle(image, transformedPoints[0], transformedPoints[1], transformedPoints[2]).draw()

image.saveAsPNG("cow.png")

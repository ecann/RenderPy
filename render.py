from image import Image, Color
from model import Model
from shape import Point, Line, Triangle

from random import randint # REMOVE ONCE SHADING IS IMPLEMENTED

width = 500
height = 300
image = Image(width, height, Color(255, 255, 255, 255))

# Load the model
model = Model('data/cow.obj')
model.normalizeGeometry()

for face in model.faces:
	points = []
	for i in face:
		# Convert vertices from world space to screen space 
		# by dropping the z-coordinate (Orthographic projection)
		vertex = model.vertices[i]
		randomColor = Color(randint(0, 255), randint(0, 255), randint(0, 255), 255)
		screenX = int((vertex[0]+1.0)*width/2.0)
		screenY = int((vertex[1]+1.0)*height/2.0)
		points.append(Point(screenX, screenY, randomColor))

	Triangle(image, points[0], points[1], points[2]).draw()

image.saveAsPNG("cow.png")

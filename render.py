from image import Image, Color

image = Image(100, 100)

for x in range(0, 100):
	for y in range(0, 100):
		if (x//10 % 2) == (y//10 % 2):
			image.setPixel(x, y, Color(2*x, 2*y, 150, 255))

image.saveAsPNG("checkerboard.png")
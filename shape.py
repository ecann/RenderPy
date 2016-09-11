""" Module for drawing geometric primitives.
"""

from image import Image, Color

class Point(object):
	""" A point in 2D space with an associated color.
		Attributes:
			x: Horizontal position
			y: Vertical position
			color: RGBA color at this point
	"""
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.color = color

class Line(object):
	""" A 2D line with color interpolated from endpoints.
		Attributes:
			image: The image to draw on
			p0: The 2D Point at the beginning of the line (with associated color)
			p1: The Point at the end of the line
	"""
	def __init__(self, image, p0, p1):
		self.image = image
		self.p0 = p0
		self.p1 = p1

	def draw(self):
		""" Draw the line using Xiaolin Wu's line algorithm."""

		x0, y0 = self.p0.x, self.p0.y
		x1, y1 = self.p1.x, self.p1.y
		c0, c1 = self.p0.color, self.p1.color

		# If the line has a slope greater than one, swap x and y
		# to make Y the driving axis. Also swap if the line is 
		# rendered from right to left.
		steep = abs(y1 - y0) > abs(x1 - x0)
		if steep:
			x0, y0, x1, y1 = y0, x0, y1, x1
		if x0 > x1:
			x0, x1, y0, y1 = x1, x0, y1, y0

		dx = x1 - x0
		dy = y1 - y0
		m = dy / dx

		def fpart(x):
			return x - int(x)
	 
		def rfpart(x):
			return 1 - fpart(x)

		def draw_endpoint(x, y, color):
			xEnd = round(x)
			yEnd = y + m * (xEnd - x)
			xGap = rfpart(x + 0.5)
			px = int(xEnd)
			py = int(yEnd)

			self.image.setPixel(px, py, Color(color.r(), color.g(), color.b(), int(color.a() * rfpart(yEnd) * xGap)))
			self.image.setPixel(px, py+1, Color(color.r(), color.g(), color.b(), int(color.a() * fpart(yEnd) * xGap)))
			return px

	    # Draw the endpoints of the line
		xstart = draw_endpoint(x0, y0, c0) + 1
		xend = draw_endpoint(x1, y1, c1)

	    # Y location of the line at this point x along the driving axis
	    # y = mx + b
		yLine = m * (xstart - x0) + y0 + m

		for x in range(xstart, xend):
			y = int(yLine)

			# Linearly interpolate the color of this pixel
			t = (x - xstart) / (xend - xstart)
			color = Color(c0.r() * (1 - t) + c1.r() * t,
						  c0.g() * (1 - t) + c1.g() * t,
						  c0.b() * (1 - t) + c1.b() * t,
						  c0.a() * (1 - t) + c1.a() * t)

			# Set pixels with alpha proportionate to how close yLine is to the center of the pixel
			if steep:
				self.image.setPixel(y, x, Color(color.r(), color.g(), color.b(), int(color.a() * rfpart(yLine))))
				self.image.setPixel(y+1, x, Color(color.r(), color.g(), color.b(), int(color.a() * fpart(yLine))))
			else:
				self.image.setPixel(x, y, Color(color.r(), color.g(), color.b(), int(color.a() * rfpart(yLine))))
				self.image.setPixel(x, y + 1, Color(color.r(), color.g(), color.b(), int(color.a() * fpart(yLine))))

			yLine += m

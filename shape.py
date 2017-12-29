""" Module for drawing geometric primitives, using only the Python standard library.
	Example Line:
		p0 = Point(10, 10, color = Color(255, 0, 0, 255))
		p1 = Point(20, 20, color = Color(0, 0, 255, 255))
		Line(p0, p1).draw(image)

	Example triangle:
		p0 = Point(10, 10, 0, Color(255, 0, 0, 255))
		p1 = Point(290, 50, 0, Color(0, 0, 255, 255))
		p2 = Point(200, 280, 0, Color(0, 255, 0, 255))
		Triangle(p0, p1, p2).draw(image)
"""

from image import Image, Color

class Point(object):
	""" A point in 2D space with an associated color.
		Attributes:
			x: Horizontal position
			y: Vertical position
			color: RGBA color at this point
	"""
	def __init__(self, x, y, z=0, color=None):
		self.x = x
		self.y = y
		self.z = z
		self.color = color

class Line(object):
	""" A 2D line with color interpolated from endpoints.
		Attributes:
			p0, p1: The endpoints of the line (with associated colors)
	"""
	def __init__(self, p0, p1):
		self.p0 = p0
		self.p1 = p1

	def draw(self, image):
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

			image.setPixel(px, py, Color(color.r(), color.g(), color.b(), int(color.a() * rfpart(yEnd) * xGap)))
			image.setPixel(px, py+1, Color(color.r(), color.g(), color.b(), int(color.a() * fpart(yEnd) * xGap)))
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
				image.setPixel(y, x, Color(color.r(), color.g(), color.b(), int(color.a() * rfpart(yLine))))
				image.setPixel(y+1, x, Color(color.r(), color.g(), color.b(), int(color.a() * fpart(yLine))))
			else:
				image.setPixel(x, y, Color(color.r(), color.g(), color.b(), int(color.a() * rfpart(yLine))))
				image.setPixel(x, y + 1, Color(color.r(), color.g(), color.b(), int(color.a() * fpart(yLine))))

			yLine += m

class Triangle(object):
	""" A triangle with color interpolated from endpoints.
		Attributes:
			image: The image to draw on
			p0, p1, p2: The points of the triangle (with associated colors)
	"""
	def __init__(self, p0, p1, p2):
		self.p0 = p0
		self.p1 = p1
		self.p2 = p2

	def edge_function(self, p0, p1, p2):
		''' Calculates the signed area of the triangle (p0, p1, p2).
			The sign of the value tells which side of the line p0p1 that p2 lies.
			Defined as the cross product of <p2-p0> and <p1-p0>
		'''
		return (p2.x - p0.x) * (p1.y - p0.y) - (p2.y - p0.y) * (p1.x - p0.x)

	def contains_point(self, point):
		''' Calculates the barycentric coordinates of the given point.
			Returns true if the point is inside this triangle,
			along with the color of that point calculated by interpolating the color
			of the triangle's vertices with the barycentric coordintes.
			Also returns the z-value of the point interpolated from the triangle's vertices.
		'''
		area = self.edge_function(self.p0, self.p1, self.p2)
		w0 =  self.edge_function(self.p1, self.p2, point)
		w1 = self.edge_function(self.p2, self.p0, point)
		w2 = self.edge_function(self.p0, self.p1, point)

		if area == 0: return False, None, None

		# Barycentric coordinates are calculated as the areas of the three sub-triangles divided
		# by the area of the whole triangle.
		alpha = w0 / area
		beta = w1 / area
		gamma = w2 / area

		# This point lies inside the triangle if w0, w1, and w2 are all positive
		if (alpha >= 0 and beta >= 0 and gamma >= 0):
			# Interpolate the color of this point using the barycentric values
			red = int(alpha*self.p0.color.r() + beta*self.p1.color.r() + gamma*self.p2.color.r())
			green = int(alpha*self.p0.color.g() + beta*self.p1.color.g() + gamma*self.p2.color.g())
			blue = int(alpha*self.p0.color.b() + beta*self.p1.color.b() + gamma*self.p2.color.b())
			alpha = int(alpha*self.p0.color.a() + beta*self.p1.color.a() + gamma*self.p2.color.a())

			# Also interpolate the z-value of this point
			zValue = int(alpha*self.p0.z + beta*self.p1.z + gamma*self.p2.z)

			return True, Color(red, green, blue, alpha), zValue

		else:
			return False, None, None

	def draw(self, image, zBuffer):
		# First calculate a bounding box for this triangle so we don't have to iterate over the entire image
		# Clamped to the bounds of the image
		xmin = max(min(self.p0.x, self.p1.x, self.p2.x), 0)
		xmax = min(max(self.p0.x, self.p1.x, self.p2.x), image.width - 1)
		ymin = max(min(self.p0.y, self.p1.y, self.p2.y), 0)
		ymax = min(max(self.p0.y, self.p1.y, self.p2.y), image.height - 1)

		# Iterate over all pixels in the bounding box, test if they lie inside in the triangle
		# If they do, set that pixel with the barycentric color of that point
		for x in range(xmin, xmax + 1):
			for y in range(ymin, ymax + 1):
				point_in_triangle, color, zValue = self.contains_point(Point(x, y, color=None))
				if point_in_triangle:
					# Check z-buffer to determine whether to draw this pixel
					if zBuffer[y*image.width + x] < zValue:
						zBuffer[y*image.width + x] = zValue
						image.setPixel(x, y, color)

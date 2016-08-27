from image import Image, Color

def drawLine(x0, y0, x1, y1, image, color):
	""" Draw a line using Xiaolin Wu's line algorithm."""

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

	def draw_endpoint(x, y):
		xEnd = round(x)
		yEnd = y + m * (xEnd - x)
		xGap = rfpart(x + 0.5)
		px = int(xEnd)
		py = int(yEnd)

		image.setPixel(px, py, Color(255, 255, 0, 255 * int(rfpart(yEnd) * xGap)))
		image.setPixel(px, py+1, Color(255, 255, 0, 255 * int(fpart(yEnd) * xGap)))
		return px

    # Draw the endpoints of the line
	xstart = draw_endpoint(x0, y0) + 1
	xend = draw_endpoint(x1, y1)

    # Y location of the line at this point x along the driving axis
    # y = mx + b
	yLine = m * (xstart - x0) + y0 + m

	for x in range(xstart, xend):
		y = int(yLine)

		# Set pixels with alpha proportionate to how close yLine is to the center of the pixel
		if steep:
			image.setPixel(y, x, Color(color.r(), color.g(), color.b(), int(color.a() * rfpart(yLine))))
			image.setPixel(y+1, x, Color(color.r(), color.g(), color.b(), int(color.a() * fpart(yLine))))
		else:
			image.setPixel(x, y, Color(color.r(), color.g(), color.b(), int(color.a() * rfpart(yLine))))
			image.setPixel(x, y + 1, Color(color.r(), color.g(), color.b(), int(color.a() * fpart(yLine))))

		yLine += m

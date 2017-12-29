# RenderPy
A software renderer written from scratch in Python 3, using only modules from the Python Standard Library.
![cow](https://raw.githubusercontent.com/ecann/RenderPy/master/images/depthCow.png)

## To Run
```python 
python3 render.py
```
## Modules
### Image.py
Contains an image class capable of generating an image and exporting it to a PNG. Images are implemented as a buffer of 32-bit RGBA pixel color data stored in a byte array. This modules uses `zlib` and `struct` for compressing and packing PNG data. 

### Shape.py
Classes representing points, lines and triangles. Each has a `draw()` method for drawing that shape in an Image. Anti-aliased lines are drawn using [Wu's Line Drawing Algorithm](https://en.wikipedia.org/wiki/Xiaolin_Wu's_line_algorithm). Triangles are drawn by iterating over a bounding box and calculating barycentric coordinates to smoothly interpolate color over the shape.

### Model.py
Class with functions for reading a `.obj` file into a stored model, retrieving vertices, faces, properties of the model.

### Render.py
Implements the rendering pipeline. Loads a model, transforms vertices, computes shading, rasterizes faces into triangles, and outputs the final image to a PNG.

## Milestones
**12/29/17** – Hidden surface removal using Z-buffer

![cola](https://raw.githubusercontent.com/ecann/RenderPy/master/images/cola_depth_comparison.png)

**12/23/17 (1 year later 😛)** – Smooth shading using vertex normals

![cow](https://raw.githubusercontent.com/ecann/RenderPy/master/images/smoothcow.png)

**12/24/16** – Simple n\*l flat shading

![cow](https://raw.githubusercontent.com/ecann/RenderPy/master/images/cow.png)

**9/13/16** – Load model from .obj file, rasterize and render with triangles

![cow](https://raw.githubusercontent.com/ecann/RenderPy/master/images/discocow.png)

**9/11/16** – Draw triangles

![cow](https://raw.githubusercontent.com/ecann/RenderPy/master/images/triangle.png)

**8/27/16** – Draw lines with Wu's Algorithm

**8/19/16** – Image module wrapping a color buffer, PNG writer

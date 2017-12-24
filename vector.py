import math
import numbers

class Vector(object):
    """ A vector with useful vector / matrix operations.
    """
    def __init__(self, *args):
        if len(args) == 0:
            self.components = (0, 0)
        else:
            self.components = args

    @property
    def x(self):
        assert(len(self) >= 1)
        return self.components[0]

    @x.setter
    def x(self, val):
        self.components = (val, self.components[1], self.components[2])

    @property
    def y(self):
        assert(len(self) >= 2)
        return self.components[1]

    @y.setter
    def y(self, val):
        self.components = (self.components[0], val, self.components[2])

    @property
    def z(self):
        assert(len(self) >= 3)
        return self.components[2]

    @z.setter
    def z(self, val):
        self.components = (self.components[0], self.components[1], val)

    def norm(self):
        """ Return the norm (magnitude) of this vector."""
        squaredComponents = sum(math.pow(comp, 2) for comp in self)
        return math.sqrt(squaredComponents)

    def normalize(self):
        """ Return a normalized unit vector from this vector."""
        magnitude = self.norm()
        return Vector(*[comp/magnitude for comp in self])

    def dot(self, other):
        """ Return the dot product of this and another vector."""
        return sum(a * b for a, b in zip(self, other))

    def cross(self, other):
        """ Return the cross product of this and another vector."""
        assert len(self) == len(other), "Vectors must be the same size."
        assert len(self) == 3, "Cross product only implemented for 3D vectors."
        return Vector((self.y*other.z - self.z*other.y), (self.z*other.x - self.x*other.z), (self.x*other.y - self.y*other.x))


    # Overrides
    def __mul__(self, other):
        """ If multiplied by another vector, return the dot product. 
            If multiplied by a number, multiply each component by other.
        """
        if type(other) == type(self):
            return self.dot(other)
        elif isinstance(other, numbers.Real):
            product = tuple(comp * other for comp in self)
            return Vector(*product)

    def __truediv__(self, other):
        if isinstance(other, numbers.Real):
            value = tuple(comp / other for comp in self)
            return Vector(*value)
    
    def __add__(self, other):
        value = tuple(a + b for a, b in zip(self, other))
        return Vector(*value)
    
    def __sub__(self, other):
        value = tuple(a - b for a, b in zip(self, other))
        return Vector(*value)

    def __len__(self):
        return len(self.components)

    def __iter__(self):
        return self.components.__iter__()
from copy import copy
from math import sqrt

class Vector:
    """Used to do vector math"""

    def __init__(self, x, y): #creates the vector object and initializses it
        self.x = x
        self.y = y
    
    def __repr__(self): #PURE returns string representation in tuple form
        return f'Vector({self.x}, {self.y})'
    
    def __add__(self, other): #PURE returns vector addition (vector)
        """
        >>> Vector(1,2)+ Vector(3,4)
        Vector(4, 6)
        
        """

        added = copy(self)
        added.x += other.x
        added.y += other.y
        return added
    
    def __sub__(self, other): #PURE returns vector subtraction (vector)
        """
        >>> Vector(3,4) - Vector(1,2)
        Vector(2, 2)
        
        """

        subtracted = copy(self)
        subtracted.x -= other.x
        subtracted.y -= other.y
        return subtracted
    
    def __mul__(self, scalar): #PURE returns scalar multiplication (vector)
        """
        >>> Vector(1, 1) * 3
        Vector(3, 3)

        """

        multiplied = copy(self)
        multiplied.x *= scalar
        multiplied.y *= scalar
        return multiplied
    
    def __rmul__(self, scalar): #PURE returns scalar multiplication (vector)
        """
        >>> 3 * Vector(1, 1)
        Vector(3, 3)
        
        """

        multiplied = copy(self)
        multiplied.x *= scalar
        multiplied.y *= scalar
        return multiplied
    
    def __rtruediv__(self, scalar): #PURE returns a scalar division (vector)
        """
        >>> 3 / Vector (1, 1)
        Vector(3.0, 3.0)

        """
        multiplied = copy(self)
        multiplied.x = scalar / self.x
        multiplied.y = scalar / self.y
        return multiplied
    
    def dot(self, other): #PURE returns vector multiplication (int)
        return (self.x * other.x) + (self.y * other.y)

    def magnitude(self): #PURE returns magniutde (int)
        """
        >>> Vector(3,4).magnitude()
        5.0

        """
        return sqrt(self.x ** 2 + self.y ** 2)
    

    def normalize(self): #PURE return the vector normalized (vector)
        """
        >>> Vector(1,0).normalize()
        Vector(1.0, 0.0)

        """


        normal = copy(self)
        magnitude = self.magnitude()
        normal.x /= magnitude
        normal.y /= magnitude
        return normal
    





# run doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
    
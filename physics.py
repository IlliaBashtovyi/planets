import math as m

'''
one pixel is one meter
time is how many times per second the calculations are done
mas is in kilograms
velocity is in meters per second
density is in kilograms per cubic meter
'''
# Function to calculate the distance between two objects
def dist(obj1, obj2):
    return m.sqrt((obj2.x - obj1.x) ** 2 + (obj2.y - obj1.y) ** 2)


# Function to calculate the distance between two points
def dist_points(x1, y1, x2, y2):
    return m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Function to add two vectors of speed
def adding_vectors(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


# vector between two objects
def vector_between(obj1, obj2):
    return (obj2.x - obj1.x)/dist(obj1, obj2), (obj2.y - obj1.y)/dist(obj1, obj2)


class OBJECT:
    def __init__(self, x, y, size, vx=0, vy=0, density=7800):
        # Initialize attributes
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.m = size ** 3 * density * 4/3 * m.pi  # mass calculation size is radius


    def move(self):
        # Method to move the object
        self.x += self.vx/time
        self.y += self.vy/time

    def acceler(self, obj):
        # Method to calculate acceleration due to another object
        G = 6.67430e-11  # Gravitational constant
        distance = dist(self, obj)
        ac = G * obj.m / distance**2
        ax = ac * (obj.x - self.x) / distance
        ay = ac * (obj.y - self.y) / distance
        self.vx += ax / time
        self.vy += ay / time

    def position(self):
        # Method to get the current position
        return self.x, self.y




time = 10

# density of steel
dens = 7800



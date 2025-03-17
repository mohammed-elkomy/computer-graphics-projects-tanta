from math import *
import sys

OO = 1000000000
class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Collosion:
    def line_polygon_intersect(self,line, vertices):
        """
        We use SAT here to check collision
        """
        lstOfVertices = line.get_vertices()
        if self.two_polygon_intersect(lstOfVertices, vertices):
            return True
        return False
    

    # Resource1 : https://gamedev.stackexchange.com/questions/43873/how-does-the-sat-collision-detection-algorithm-work
    # Resource2 : https://gamedevelopment.tutsplus.com/tutorials/collision-detection-using-the-separating-axis-theorem--gamedev-169
    
    def two_polygon_intersect(self, VerticesA ,VerticesB):
        """
        separating axis theorem implementation
        this function check if there's a collision between any two convex polygon or not
        Vertices : 2D List , Vertices[i][0] -> x, Vertices[i][1] -> y
        """
        # First we need to find all edges in shape A
        n = len(VerticesA)
        for i in range(n):
            p1 = VerticesA[i]
            p2 = VerticesA[(i+1) % n]
            axis = self.get_unit_normal_vector(p1,p2)
            # for Each Axis we need to project all points from shape A, and all points from shape B , then compare
            projA = self.projectVertices(VerticesA, axis)
            projB = self.projectVertices(VerticesB, axis)
            #There's a gap if (maxB < minA) or (maxA < minB) -->> return False No intersection
            if projB[1] < projA[0] or projA[1] < projB[0]:
                return False
        n = len(VerticesB)
        for i in range(n):
            p1 = VerticesB[i]
            p2 = VerticesB[(i+1) % n]
            axis = self.get_unit_normal_vector(p1,p2)
            # for Each Axis we need to project all points from shape A, and all points from shape B , then compare
            projA = self.projectVertices(VerticesA, axis)
            projB = self.projectVertices(VerticesB, axis)
            #There's a gap if (maxB < minA) or (maxA < minB) -->> return False No intersection
            if projB[1] < projA[0] or projA[1] < projB[0]:
                return False
        return True
            

    def projectVertices(self,vertices,axis):
        """
        This function project a list of vertices on axis by using dot product 
        Then return the max point and min point on axis
        """
        minA, maxA = OO, -OO
        # to project point on axis , just do dot product
        for v in vertices:
            proj = axis[0]*v[0] + axis[1]*v[1]
            if proj < minA:
                minA = proj
            if proj > maxA:
                maxA = proj
        return (minA,maxA)
    
    def get_unit_normal_vector(self,p1,p2):
        """"
        return unit normal vector of edge p1p2
        """
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        magnitude = sqrt(dx**2 + dy**2)
        if magnitude != 0: # To avoid division by zero
            dx = dx/magnitude
            dy = dy/magnitude
        return [-dy,dx]

col = Collosion()

def test_car_walls(carModel, walls):
    """
    this method use SAT to check car & walls collision
    """
    vertices = carModel.get_vertices()
    for i in walls:
        if col.line_polygon_intersect(i,vertices):
            return True
    return False

def test_car_coin(carModel, coins):
    """
    this method use SAT to check car & coin collision
    """
    carVertices = carModel.get_vertices()
    for i in coins:
        if i.collected == True:
            continue
        coinVertices = i.get_vertices()
        if col.two_polygon_intersect(carVertices,coinVertices):
            i.collected = True
            return True
    return False

def test_car_bomb(carModel,bombs):
    """
    this method use SAT to check car & bomb collision
    """
    carVertices = carModel.get_vertices()
    for i in bombs:
        if i.collected == True:
            continue
        bombVertices = i.get_vertices()
        if col.two_polygon_intersect(carVertices,bombVertices) == True:
            i.collected = True
            return True
    return False

def test_car_health(carModel,health):
    """
    this method use SAT to check car & health collision
    """
    carVertices = carModel.get_vertices()
    for i in health:
        if i.collected:
            continue
        healthVertices = i.get_vertices()
        if col.two_polygon_intersect(carVertices,healthVertices):
            i.collected = True
            return True
    return False

def test_car_finish(carModel,finsh):
    """
    this method use SAT to check car & finishLine collision
    """
    carVertices = carModel.get_vertices()
    for i in finsh:
        healthVertices = i.get_vertices()
        if col.two_polygon_intersect(carVertices,healthVertices):
            return True
    return False


# TESTING 
if __name__ == "__main__":
    c = Collosion()
    if c.two_polygon_intersect([[0,0],[10,0],[10,10],[0,10]], [[20,0],[30,0],[30,10],[20,10]]) == False:
        print("True")
    else:
        print("Expected True output False")
    if c.two_polygon_intersect([[0,0],[10,0],[10,10],[0,10]], [[5,0],[15,0],[15,10],[5,10]]) == True: 
        print("True")
    else:
        print("Expected True output False")
    if c.two_polygon_intersect([[20.0, 50.0], [20.0, 20.0], [80.0, 20.0], [80.0, 50.0]], [[100, 350], [100, 400], [150, 400], [150, 350]]) == False:
        print("True")
    else:
        print("Expected True output False")
    if c.two_polygon_intersect([[327.8437342690493, 68.23378448111289], [354.661908380755, 54.78813323938297], [381.5532108642146, 108.42448146279385], [354.7350367525089, 121.87013270452377]], [[100, 350], [100, 400], [150, 400], [150, 350]]) == False: 
        print("True")
    else:
        print("Expected True output False")
    
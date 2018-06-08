import math
''' At altitude of 122m vertical fov is 133m horizontal fov is 200m '''
''' reference point for distance in dd is start of tessalation -> min lat/lon'''

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

def onSegment(p1, q1, a):
    return a.x <= max(p1.x, q1.x) and a.x >= min(p1.x, q1.x) and \
        a.y <= max(p1.y, q1.y) and a.x >= min(p1.x, q1.x)
        
def orientation(p1, p2, p3):
    val = (p2.y - p1.y) * (p3.x - p2.x) - (p3.y - p2.y) * (p2.x - p1.x)
    if val == 0:
        return 0 #points are colinear
    elif val > 0:
        return 1 #clockwise
    elif val < 0:
        return 2 #counterclockwise

def intersect(p1, q1, p2, q2):
    #general case
    if (orientation(p1, q1, p2) != orientation(p1, q1, q2)) and \
        (orientation(p2, q2, p1) != orientation(p2, q2, q1)):
        return True    
    #special cases -> p1,q1,p2,q2 are colinear and x,y projections intersect
    if orientation(p1, q1, p2) == 0 and onSegment(p1, q1, p2):
        return True
    if orientation(p1, q1, q2) == 0 and onSegment(p1, q1, q2):
        return True    
    if orientation(p2, q2, p1) == 0 and onSegment(p2, q2, p1):
        return True
    if orientation(p2, q2, q1) == 0 and onSegment(p2, q2, q1):
        return True    
    return False

def isInside(polygon, p):
    if len(polygon) < 3:
        return false
    count = 0
    i = 0
    while True:
        nxt = (i + 1) % len(polygon)
        if intersect(polygon[i], polygon[nxt], p, Point(10000, p.y)):
            #check if p is colinear with line segment then if its on segment
            if(orientation(polygon[i], polygon[nxt], p) == 0):
                return onSegment(polygon[i], polygon[nxt], p)
            count += 1
        i = nxt
        if i == 0:
            break
    #return true if odd        
    return count % 2 == 1 

def generateWaypoints(polygon, lats, lons):
    intervalX = 0.0022
    intervalY = 0.0006
    y = min(lats) + intervalY/2
    while y < max(lats) + intervalY/2:
        x = min(lons) + intervalX/2
        while x < max(lons) + intervalY/2:
            if isInside(polygon, Point(x, y)):
                outFile.write(str(y) + ', ' + str(x) + '\n')
            x += intervalX
        y += intervalY
    
polygon1 = []
lons = []
lats = []
outFile = open("midpoints2.csv", "w")
with open("farm1.csv", "r") as fd:
    entries = fd.readlines()
for line in entries:
    x = float(line.split('\n')[0].split(',')[1])
    y = float(line.split('\n')[0].split(',')[0])
    polygon1.append(Point(x, y))
    lons.append(x)
    lats.append(y)

#print(isInside(polygon1, Point(-113.557, 53.491)))
generateWaypoints(polygon1, lats, lons)
outFile.close()

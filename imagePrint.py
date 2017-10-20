from PIL import Image, ImageDraw
from random import randint
import math

class Point:
    def __init__(self, v, color):
        self.x = v[0]
        self.y = v[1]
        self.z = v[2]
        self.color = color
     
    def lerp(a, b, t):
        return Point([Math.flerp(a.x, b.x, t), Math.flerp(a.y, b.y, t), Math.flerp(a.z, b.z, t)], Math.lerpColors(a.color, b.color, t))

    def copy (a):
        b = Point([a.x, a.y, a.z], a.color)
        return b

class Math:

    def flerp(a, b, t):
        return a + (b - a)*t

    def lerpColors(col1, col2, t):
        x = []
        for i in range(0, len(col1)):
            y=Math.flerp(col1[i], col2[i], t)
            x.append(y)
        return int(round(x[0])),int(round(x[1])), int(round(x[2]))

    def lerpVect(v1, v2, length):
        a = int(round(p1.x + (point2.x-p1.x)*length))
        b = int(round(p1.y + (point2.y-p1.y)*length))
        return [a,b]

    def sortVec(v1, v2, v3):
        x = [v1.y,v2.y,v3.y]
        x = sorted(x)

        if v2.y == x[1]:
            temp=v1
            v1=v2
            v2=temp

        if v3.y == x[1]:
            temp=v1
            v1=v3
            v3=temp
        if v2.y == x[0]:
            temp = v2
            v2=v3
            v3=temp
        return v1, v2, v3

class Model:

    def __init__(self, points, edges, triangles):

        self.points = points
        self.edges = edges
        self.triangles = triangles

        # for i in range(0, len(self.edges)):
        #     pointA = self.points[self.edges[i][0]].copy()
        #     pointB = self.points[self.edges[i][1]].copy()
        #     pointA=canvas.perspective(pointA)
        #     pointB=canvas.perspective(pointB)
        #     canvas.drawLine(pointA, pointB)

    # def edges():
    #     pass


    # def triangles():
    #     pass





class canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        size = [width, height]
        self.backingImage =Image.new('RGB', size, (255, 255, 255))
        self.drawer = ImageDraw.Draw(self.backingImage)
 
    def drawModel(self, m, wireframeMode):



        for i in range(0, len(m.triangles)):
            pointA = m.points[m.triangles[i][0]].copy()
            pointB = m.points[m.triangles[i][1]].copy()
            pointC = m.points[m.triangles[i][2]].copy()
            pointA=self.perspective(pointA)
            pointB=self.perspective(pointB)
            pointC=self.perspective(pointC)
            self.drawTriangle(pointA, pointB, pointC)

        if wireframeMode == True:
            for i in range(0, len(m.edges)):
                pointA = m.points[m.edges[i][0]].copy()
                pointB = m.points[m.edges[i][1]].copy()
                pointA=self.perspective(pointA)
                pointB=self.perspective(pointB)
                self.drawLine(pointA, pointB)

    def wireCube(self, point1, point2, point3, point4, point5, point6, point7, point8):

        screen.drawLine(point1, point2)
        screen.drawLine(point1, point3)
        screen.drawLine(point2, point4)
        screen.drawLine(point3, point4)

        screen.drawLine(point5, point6)
        screen.drawLine(point5, point7)
        screen.drawLine(point6, point8)
        screen.drawLine(point7, point8)

        screen.drawLine(point1, point5)
        screen.drawLine(point2, point6)
        screen.drawLine(point3, point7)
        screen.drawLine(point4, point8)

    def perspective(self, p):
        mp = (self.width/2, self.height/2)
      #  p1.x = Math.flerp(p1.x, mp[0], (p1.z/10*0.0001))
       # p1.y = Math.flerp(p1.y, mp[1], (p1.z/10*0.0001))
        p.x = p.x + ((mp[0] - p.x)*p.z*0.01)
        p.y = p.y + ((mp[1] - p.y)*p.z*0.01)

        return p

    def setPixel(self, a):
        self.drawer.point((int(round(a.x)), int(round(a.y))), fill=a.color)

    def drawLine(self, point1, point2):
        p1 = point1.copy()
        p2 = point2.copy()
        # p1 = self.perspective(p1)
        # p2 = self.perspective(p2)
        longest_axis = math.ceil(max(abs(p2.x - p1.x), abs(p2.y - p1.y)))

        for i in range(0, int(longest_axis)):
            point = Point.lerp(p1, p2, i / longest_axis)
            self.setPixel(point)
            
    def drawRectangle(x, y, width, height, col1, col2, col3, col4):
        topLineStart = [x, y]
        topLineEnd = [x, y + width - 1]

        for i in range (0, height):
            color1 = Math.lerpColors(col1, col3, i/height)
            color2 = Math.lerpColors(col2, col4, i/height)
            Math.drawLine(topLineStart, topLineEnd, color1, color2)
            topLineStart[0] += 1
            topLineEnd[0] += 1

    def drawTriangle(self, point1, point2, point3):
        p1 = point1.copy()
        p2 = point2.copy()
        p3 = point3.copy()
        # p1 = self.perspective(p1)
        # p2 = self.perspective(p2)
        # p3 = self.perspective(p3)
        p1, p2, p3 = Math.sortVec(p1, p2, p3)


        # p1 = self.perspective(p1)
        # p2 = self.perspective(p2)
        # p3 = self.perspective(p3)

        spanLengthV3 = abs(p1.y - p3.y)
        spanLengthV2 = abs(p1.y - p2.y)
        spanLength = abs(max(p1.x, p1.y))
        if spanLengthV2 == 0:
            spanLengthV2 = 1
        if spanLengthV3 == 0:
            spanLengthV3 = 1

        t=0
        if (p2.y-p3.y) != 0:

            t = abs((p1.y-p3.y)/(p2.y-p3.y))
        p4 = Point.lerp(p3, p2, t)


        for i in range(0, int(spanLengthV2) + 1):
            a = Point.lerp(p2,p1, i/spanLengthV2)
            b = Point.lerp(p2,p4, i/spanLengthV2)
            #a = self.perspective(a)
            #b = self.perspective(b)
            self.drawLine(a, b)

        for i in range(0, int(spanLengthV3) + 1):
            a = Point.lerp(p3,p1, i/spanLengthV3)
            b = Point.lerp(p3,p4, i/spanLengthV3)
            #a = self.perspective(a)
            #b = self.perspective(b)
            self.drawLine(a, b)

    def saveImage(self, name):
        self.backingImage.save(name + ".png")



width = 1000
height = 1000
screen = canvas(width, height)
# color1 = (randint(0, rgb), randint(0,rgb), randint(0,rgb))
# color2 = (randint(0, rgb), randint(0,rgb), randint(0,rgb))
# color3 = (randint(0, rgb), randint(0,rgb), randint(0,rgb))
# color4 = (25, 90, 100)

vec = []
file = open("untitled.obj","r") #opens file with name of "test.txt"
content = file.readlines()
v = []
content = [x.strip() for x in content]
for i in range(0, len(content)):
    if content[i].startswith('v'):
        v.append(content[i])
x= []
y=[]
for i in range(0, 8):
    v[i]=v[i][2:]
    vec.append(list(map(float, v[i].split())))

    print(vec)


# vec1 = [200, 200, 0]
# vec2 = [200, 400, 0]
# vec3 = [400, 200, 0]
# vec4 = [400, 400, 0]
# vec5 = [200, 200, 20]
# vec6 = [200, 400, 20]
# vec7 = [400, 200, 20]
# vec8 = [400, 400, 20]

color1 = [50, 50, 50]
color2 = [200, 200, 200]

p1 = Point(vec[0], color1)
p2 = Point(vec[1], color1)
p3 = Point(vec[2], color1)
p4 = Point(vec[3], color1)

p5 = Point(vec[4], color2)
p6 = Point(vec[5], color2)
p7 = Point(vec[6], color2)
p8 = Point(vec[7], color2)

points = [p1, p2, p3, p4, p5, p6, p7, p8]
edges = [(0,1), (0,2), (1,3), (2,3), (4,5), (4,6), (5,7), (6,7), (0,4), (1, 5), (2,6), (3,7)]
triangles = [(7,4,6), (5,4,7), (0,2,4), (2,4,6), (3,7,6), (2,3,6), (0,1,5), (5,0,4), (1,3,5), (3,5,7), (0,1,2), (1,2,3)]


cube = Model(points, edges, triangles)
screen.drawModel(cube, True)
# cube.points = [point1, point2, point3, point4, point5, point6, point7, point8]

# # #baksidan
# screen.drawTriangle(point8, point5, point7)
# screen.drawTriangle(point6, point5, point8)

# screen.drawTriangle(point1, point3, point5)
# screen.drawTriangle(point3, point5, point7)

# #högra sidan
# screen.drawTriangle(point4, point8, point7)
# screen.drawTriangle(point3, point4, point7)

# #vänstra sidan
# screen.drawTriangle(point1, point2, point6)
# screen.drawTriangle(point6, point1, point5)

# #undersidan
# screen.drawTriangle(point2, point4, point6)
# screen.drawTriangle(point4, point6, point8)
# #framsida
# screen.drawTriangle(point1, point2, point3)
# screen.drawTriangle(point2, point3, point4)


# screen.wireCube(cube.p1, cube.p2, cube.p3, cube.p4, cube.p5, cube.p6, cube.p7, cube.p8)

screen.saveImage("beautiful")

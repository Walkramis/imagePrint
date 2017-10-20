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


class canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        size = [width, height]
        self.backingImage =Image.new('RGB', size, (255, 255, 255))
        self.drawer = ImageDraw.Draw(self.backingImage)
 

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
        p1 = self.perspective(p1)
        p2 = self.perspective(p2)
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


# screen.drawTriangle(point1, point2, point3)
# screen.drawTriangle(point2, point3, point4)
# screen.drawTriangle(point8, point5, point7)
# screen.drawTriangle(point6, point1, point5)
# screen.drawTriangle(point7, point1, point3)
# screen.drawTriangle(point4, point6, point8)
# screen.drawTriangle(point2, point4, point3)
# screen.drawTriangle(point4, point8, point7)
# screen.drawTriangle(point8, point6, point3)
# screen.drawTriangle(point1, point2, point6)
# screen.drawTriangle(point7, point5, point1)
# screen.drawTriangle(point4, point2, point6)

vec1 = [200, 200, 0]
vec2 = [200, 400, 0]
vec3 = [400, 200, 0]
vec4 = [400, 400, 0]
vec5 = [200, 200, 20]
vec6 = [200, 400, 20]
vec7 = [400, 200, 20]
vec8 = [400, 400, 20]

color1 = [50, 50, 50]
color2 = [200, 200, 200]

point1 = Point(vec1, color1)
point2 = Point(vec2, color1)
point3 = Point(vec3, color1)
point4 = Point(vec4, color1)

point5 = Point(vec5, color2)
point6 = Point(vec6, color2)
point7 = Point(vec7, color2)
point8 = Point(vec8, color2)

screen.wireCube(point1, point2, point3, point4, point5, point6, point7, point8)

screen.saveImage("beautiful")

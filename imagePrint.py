from PIL import Image, ImageDraw
from random import randint
import math

class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
     
    def lerp(a, b, t):
        return Point(Math.flerp(a.x, b.x, t), Math.flerp(a.y, b.y, t), Math.lerpColors(a.color, b.color, t))

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
        a = int(round(p1.x + (p2.x-p1.x)*length))
        b = int(round(p1.y + (p2.y-p1.y)*length))
        return [a,b]

    def sortVec(v1, v2, v3):
        x = [p1.y,p2.y,p3.y]
        x = sorted(x)

        if p2.y == x[1]:
            temp=v1
            v1=v2
            v2=temp

        if p3.y == x[1]:
            temp=v1
            v1=v3
            v3=temp
        if p2.y == x[0]:
            temp = v2
            v2=v3
            v3=temp
        return v1, v2, v3


class canvas:
    def __init__(self, width, height, filler):
        self.width = width
        self.height = height
        size = [width, height]
        self.backingImage =Image.new('RGB', size, (255, 255, 255))
        self.drawer = ImageDraw.Draw(self.backingImage)
 
    def setPixel(self, a):
        #print(a.x, a.y)
        self.drawer.point((int(round(a.x)), int(round(a.y))), fill=a.color)

    def drawLine(self, p1, p2):
        longest_axis = math.ceil(max(abs(p2.x - p1.x), abs(p2.y - p1.y)))
        for i in range(0, int(longest_axis)):
            point = Point.lerp(p1, p2, i / int(longest_axis))
            self.setPixel(point)

 #   def drawLine(self, p1, p2):
        xLength = abs(p1.x - p2.x)
        yLength = abs(p1.y - p2.y)

        maxLengthRounded = int(round(max(xLength, yLength)))
        maxLength = max(xLength, yLength)
        #print(p1.x, p2.x, maxLength, xLength)
        xParam = 1
        yParam = 1
        xRatio = 1
        yRatio = 1
        if p1.x > p2.x:
            xParam = -1
        if p1.y > p2.y:
            yParam = -1        

        if max(xLength, yLength) == yLength and yLength != xLength:
            xRatio=xLength/yLength
            yRatio=1

        if max(xLength, yLength) == xLength and xLength != yLength:
            xRatio=1
            yRatio=yLength/xLength
        x=[]
        y=[]

        for i in range(0, maxLengthRounded):
            if maxLength == 0:
                maxLength = 1
            a = Point.lerp(p1,p2, i/maxLength)
            #print(a.x, p1.x, p2.x)
            self.setPixel(a)
            
    def drawRectangle(x, y, width, height, col1, col2, col3, col4):
        topLineStart = [x, y]
        topLineEnd = [x, y + width - 1]

        for i in range (0, height):
            color1 = Math.lerpColors(col1, col3, i/height)
            color2 = Math.lerpColors(col2, col4, i/height)
            Math.drawLine(topLineStart, topLineEnd, color1, color2)
            topLineStart[0] += 1
            topLineEnd[0] += 1

    def drawTriangle(self, p1, p2, p3):

        p1, p2, p3 = Math.sortVec(p1, p2, p3)
        
        spanLengthV3 = abs(p1.y - p3.y)
        spanLengthV2 = abs(p1.y - p2.y)
        spanLength = abs(max(p1.x, p1.y))
        if spanLengthV2 == 0:
            spanLengthV2 = 1
        if spanLengthV3 == 0:
            spanLengthV3 = 1

        t = abs((p1.y-p3.y)/(p2.y-p3.y))
        p4 = Point.lerp(p3, p2, t)


        for i in range(0, spanLengthV2 + 1):
            a = Point.lerp(p2,p1, 1/spanLengthV2*i)
            b = Point.lerp(p2,p4, 1/spanLengthV2*i)
            self.drawLine(a, b)

        for i in range(0, spanLengthV3 + 1):
            a = Point.lerp(p3,p1, 1/spanLengthV3*i)
            b = Point.lerp(p3,p4, 1/spanLengthV3*i)
            self.drawLine(a, b)

    def saveImage(self, name):
        self.backingImage.save(name + ".png")

width = 1920
height = 1080
screen = canvas(width, height, " ")
v1 = [randint(0, width), randint(0,height)]
v2 = [randint(0, width), randint(0,height)]
v3 = [randint(0, width), randint(0,height)]

color1 = (255, 125, 79)
color2 = (14, 255, 124)
color3 = (67, 28, 255)
color4 = (25, 90, 100)


p1 = Point(v1[0], v1[1], color1)
p2 = Point(v2[0], v2[1], color2)
p3 = Point(v3[0], v3[1], color3)

#screen.drawLine(p2, p3)
screen.drawTriangle(p1, p2, p3)
#screen.drawTriangle(v1, v2, v3, color1, color2, color3)
#screen.drawLine(v1, v2, color1, color1)
#screen.drawLine(v1, v3, color1, color1)
#screen.drawLine(v2, v3, color1, color1)
#width = 800
#height = 600
#screen.drawRectangle(p1.x, p1.y, height, width, color1, color2, color3, color4)
screen.saveImage("beautiful")

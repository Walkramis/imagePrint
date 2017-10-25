from PIL import Image, ImageDraw
from random import randint
import math


class Point:
    def __init__(self, coordinate, color):
        self.coordinate = coordinate
        self.color = color
     
    def lerp(a, b, t):
        return Point(vec3(Math.flerp(a.coordinate.x, b.coordinate.x, t), Math.flerp(a.coordinate.y, b.coordinate.y, t), Math.flerp(a.coordinate.z, b.coordinate.z, t)), Math.lerpColors(a.color, b.color, t))

    def copy (a):
        vec=a.coordinate.copy()
        b = Point(vec, a.color)
        return b

class Math:

    def flerp(a, b, t):
        return a + (b - a)*t

    # def lerpColors(col1, col2, t):
        # x=()        
        # for i in range(0, len(col1)):
        #     y=Math.flerp(col1[i], col2[i], t)
        #     x[i]=y
        # return int(x[0]),int(x[1]), int(x[2])
    def lerpColors(col1, col2, t):
        return (int(Math.flerp(col1[0], col2[0], t)),
               int(Math.flerp(col1[1], col2[1], t)),
               int(Math.flerp(col1[2], col2[2], t)))

    def sortVec(v1, v2, v3):
        x = [v1.coordinate.y,v2.coordinate.y,v3.coordinate.y]
        x = sorted(x)

        if v2.coordinate.y == x[1]:
            temp=v1.copy()
            v1=v2
            v2=temp

        if v3.coordinate.y == x[1]:
            temp=v1.copy()
            v1=v3
            v3=temp
        if v2.coordinate.y == x[0]:
            temp = v2.copy()
            v2=v3
            v3=temp
        return v1, v2, v3

class vec3:
    def __init__(self, x, y, z):
        self.x=x
        self.y=y
        self.z=z

    def copy(a):
        b=vec3(a.x, a.y,a.z)
        return b

    def __mul__(self, other):
        x=self.x*other.x
        y=self.y*other.y
        z=self.z*other.z
        return vec3(x, y, z)

    def __add__(self, other):
        x=self.x+other.x
        y=self.y+other.y
        z=self.z+other.z
        return vec3(x, y, z)

class Obj:
    def __init__(self, filename):
        self.filename = filename
        file = open(self.filename + ".obj","r") #opens file with name of "test.txt"
        content = file.readlines()
        v = []
        vec = []
        f = []
        x = []
        y = []

        content = [x.strip() for x in content]

        for i in range(0, len(content)):
            if content[i].startswith('v ') == True:
                v.append(content[i])
            if content[i].startswith('f'):
                f.append(content[i])

        for i in range(0, len(v)):
            v[i]=v[i][2:]
            vec.append(list(map(float, v[i].split())))



        fv=[]
        ft=[]
        fn=[]
        z=[]
        a=[]
        b=[]
        c=[]
        d = []

        for i in range(0, len(f)):
            f[i]=f[i][2:]
            y.append(list(f[i].split()))
            a.append(list(y[i][0].split("/")))
            b.append(list(y[i][1].split("/")))
            c.append(list(y[i][2].split("/")))
            d.append(list(y[i][0].split("/")))

            d[i][0]=int(a[i][0]) - 1
            d[i][1]=int(b[i][0]) - 1
            d[i][2]=int(c[i][0]) - 1
            fv.append(tuple(d[i]))

            if a[0][1] != '':
                d[i][0]=int(a[i][1]) - 1
                d[i][1]=int(b[i][1]) - 1
                d[i][2]=int(c[i][1]) - 1
                ft.append(tuple(d[i]))

            d[i][0]=int(a[i][2]) - 1
            d[i][1]=int(b[i][2]) - 1
            d[i][2]=int(c[i][2]) - 1
            fn.append(tuple(d[i]))


        color2 = [200, 200, 200]
        color1 = [100, 100, 100]
        objPoint=[]

        for i in range(0, len(vec)): 
            objPoint.append(Point(vec3(vec[i][0], vec[i][1], vec[i][2]), color1))


        self.points = objPoint
        self.edges = [(0,1), (0,2), (1,3), (2,3), (4,5), (4,6), (5,7), (6,7), (0,6), (1, 7), (2,4), (3,5)]
        self.triangles = fv


class Model:

    def __init__(self, points, edges, triangles):

        self.points = points
        self.edges = edges
        self.triangles = triangles

class canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        size = [width, height]
        self.backingImage =Image.new('RGB', size, (0, 0, 0))
        self.drawer = ImageDraw.Draw(self.backingImage)
        self.zBuffer = []
        drawDistance = 1000
        self.zBuffer = [[drawDistance for x in range(width)] for y in range(height)]
 
    def drawModel(self, m, model_translate, model_scale, view_translate, drawFunction):



        for i in range(0, len(m.triangles)):

            pointA = m.points[m.triangles[i][0]].copy()
            pointB = m.points[m.triangles[i][1]].copy()
            pointC = m.points[m.triangles[i][2]].copy()

            pointA.coordinate=pointA.coordinate*model_scale
            pointB.coordinate=pointB.coordinate*model_scale
            pointC.coordinate=pointC.coordinate*model_scale
  
            translation = model_translate + view_translate

            pointA.coordinate = pointA.coordinate + translation
            pointB.coordinate = pointB.coordinate + translation
            pointC.coordinate = pointC.coordinate + translation

            pointA=self.perspective(pointA)
            pointB=self.perspective(pointB)
            pointC=self.perspective(pointC)
            drawFunction(pointA, pointB, pointC)

    def wireframe(self, pointA, pointB, pointC):
        self.drawLine(pointA, pointB)
        self.drawLine(pointB, pointC)
        self.drawLine(pointA, pointA)

    def perspective(self, point):
        mp = (self.width/2, self.height/2)
        p=point.copy()
        p.coordinate.x = p.coordinate.x + ((mp[0] - p.coordinate.x)*p.coordinate.z*0.0005)
        p.coordinate.y = p.coordinate.y + ((mp[1] - p.coordinate.y)*p.coordinate.z*0.0005)

        return p

    def setPixel(self, a):
        
        x=int(round(a.coordinate.x))
        y=int(round(a.coordinate.y))
        z=int(round(a.coordinate.z))
        color = (300-z, 300-z, 300-z)
        if self.zBuffer[x][y] > z:
            self.zBuffer[x][y] = z
            self.drawer.point((x, y), fill=color)


    def drawLine(self, p1, p2):

        longest_axis = (max(abs(p2.coordinate.x - p1.coordinate.x), abs(p2.coordinate.y - p1.coordinate.y)))
        
        if longest_axis == 0:
            longest_axis = 1
        rounded_axis = math.ceil(longest_axis)
        for i in range(0, int(rounded_axis) +2):
                point = Point.lerp(p1, p2, i / (rounded_axis) -1/rounded_axis)
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

    def drawTriangle(self, p1, p2, p3):

        p1, p2, p3 = Math.sortVec(p1, p2, p3)

        spanLengthV3 = abs(p1.coordinate.y - p3.coordinate.y)
        spanLengthV2 = abs(p1.coordinate.y - p2.coordinate.y)

        t=0
        if (p2.coordinate.y-p3.coordinate.y) != 0:

            t = abs((p1.coordinate.y-p3.coordinate.y)/(p2.coordinate.y-p3.coordinate.y))

        p4 = Point.lerp(p3, p2, t)
        spanV3 = math.ceil(spanLengthV3)
        spanV2 = math.ceil(spanLengthV2)


        if spanV2 == 0:
            spanV2 = 1
        for i in range(0, int(spanV2+1)):
            a = Point.lerp(p2,p1, i/(spanV2))
            b = Point.lerp(p2,p4, i/(spanV2))

            self.drawLine(a, b)


        if spanV3 == 0:
            spanV3=1
        for i in range(0, int(spanV3+1)):
            a = Point.lerp(p3,p1, i/(spanV3))
            b = Point.lerp(p3,p4, i/(spanV3))
            self.drawLine(a, b)

    def saveImage(self, name):
        self.backingImage.save(name + ".png")



width = 1000
height = 1000
screen = canvas(width, height)

hjul1 = vec3(0,200,0)
hjul2 = vec3(200,200,00)
hjul3 = vec3(0,200,100)
hjul4 = vec3(200,200,100)

vTranslate = vec3(0, 0, 0)

mScale = vec3(0.25, 0.25, 0.25)

loadedObject = Obj("hjul2")
cube = Model(loadedObject.points, loadedObject.edges, loadedObject.triangles)
screen.drawModel(cube, hjul1, mScale, vTranslate, screen.drawTriangle)
screen.drawModel(cube, hjul2, mScale, vTranslate, screen.drawTriangle)
screen.drawModel(cube, hjul3, mScale, vTranslate, screen.drawTriangle)
screen.drawModel(cube, hjul4, mScale, vTranslate, screen.drawTriangle)


screen.saveImage("beautiful")
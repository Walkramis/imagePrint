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

        for i in range(0, len(v)):
            v[i]=v[i][2:]
            vec.append(list(map(float, v[i].split())))

        for i in range(0, len(content)):
            if content[i].startswith('f'):
                f.append(content[i])


        for i in range(0, len(f)):
            f[i]=f[i][2:]

        fv=[]
        ft=[]
        fn=[]
        z=[]
        a=[]
        b=[]
        c=[]
        d = []

        for i in range(0, len(f)):
            y.append(list(f[i].split()))
            a.append(list(y[i][0].split("/")))
            b.append(list(y[i][1].split("/")))
            c.append(list(y[i][2].split("/")))
            d.append(list(y[i][0].split("/")))


        for i in range(0, len(f)):
            d[i][0]=int(a[i][0]) - 1
            d[i][1]=int(b[i][0]) - 1
            d[i][2]=int(c[i][0]) - 1
            fv.append(tuple(d[i]))

        if a[0][1] != '':
            for i in range(0, len(f)):
                d[i][0]=int(a[i][1]) - 1
                d[i][1]=int(b[i][1]) - 1
                d[i][2]=int(c[i][1]) - 1
                ft.append(tuple(d[i]))

        for i in range(0, len(f)):
            d[i][0]=int(a[i][2]) - 1
            d[i][1]=int(b[i][2]) - 1
            d[i][2]=int(c[i][2]) - 1
            fn.append(tuple(d[i]))

        color2 = [200, 200, 200]
        color1 = [100, 100, 100]
        objPoint=[]
        for i in range(0, len(vec)):
            objPoint.append(Point(vec[i], color1))


        self.points = objPoint
        self.edges = [(0,1), (0,2), (1,3), (2,3), (4,5), (4,6), (5,7), (6,7), (0,6), (1, 7), (2,4), (3,5)]
        self.triangles = fv


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
        self.backingImage =Image.new('RGB', size, (0, 0, 0))
        self.drawer = ImageDraw.Draw(self.backingImage)
        self.zBuffer = []
        drawDistance = 1000
        self.zBuffer = [[drawDistance for x in range(width)] for y in range(height)]
 
    def drawModel(self, m, model_translate, model_scale, view_translate, wireframeMode):



        if wireframeMode == True:
            for i in range(0, len(m.triangles)):
                pointA = m.points[m.triangles[i][0]].copy()
                pointB = m.points[m.triangles[i][1]].copy()
                pointC = m.points[m.triangles[i][2]].copy()

                pointA.x*=model_scale[0]
                pointB.x*=model_scale[0]
                pointC.x*=model_scale[0]
                pointA.y*=model_scale[1]
                pointB.y*=model_scale[1]
                pointC.y*=model_scale[1]
                pointA.z*=model_scale[2]
                pointB.z*=model_scale[2]
                pointC.z*=model_scale[2]
                
                pointA.x+= model_translate[0] + view_translate[0]
                pointB.x+= model_translate[0] + view_translate[0]
                pointC.x+= model_translate[0] + view_translate[0]

                pointA.y+= model_translate[1] + view_translate[1]
                pointB.y+= model_translate[1] + view_translate[1]
                pointC.y+= model_translate[1] + view_translate[1]

                pointA.y+= model_translate[2] + view_translate[2]
                pointB.y+= model_translate[2] + view_translate[2]
                pointC.y+= model_translate[2] + view_translate[2]


                pointA=self.perspective(pointA)
                pointB=self.perspective(pointB)
                pointC=self.perspective(pointC)
                self.drawLine(pointA, pointB)
                self.drawLine(pointB, pointC)
                self.drawLine(pointC, pointA)

        else:
            for i in range(0, len(m.triangles)):

                pointA = m.points[m.triangles[i][0]].copy()
                pointB = m.points[m.triangles[i][1]].copy()
                pointC = m.points[m.triangles[i][2]].copy()

                pointA.x*=model_scale[0]
                pointB.x*=model_scale[0]
                pointC.x*=model_scale[0]
                pointA.y*=model_scale[1]
                pointB.y*=model_scale[1]
                pointC.y*=model_scale[1]
                pointA.z*=model_scale[2]
                pointB.z*=model_scale[2]
                pointC.z*=model_scale[2]

                pointA.x+= model_translate[0] + view_translate[0]
                pointB.x+= model_translate[0] + view_translate[0]
                pointC.x+= model_translate[0] + view_translate[0]

                pointA.y+= model_translate[1] + view_translate[1]
                pointB.y+= model_translate[1] + view_translate[1]
                pointC.y+= model_translate[1] + view_translate[1]

                pointA.z+= model_translate[2] + view_translate[2]
                pointB.z+= model_translate[2] + view_translate[2]
                pointC.z+= model_translate[2] + view_translate[2]

                pointA=self.perspective(pointA)
                pointB=self.perspective(pointB)
                pointC=self.perspective(pointC)
                self.drawTriangle(pointA, pointB, pointC)

    def perspective(self, p):
        mp = (self.width/2, self.height/2)

        p.x = p.x + ((mp[0] - p.x)*p.z*0.0005)
        p.y = p.y + ((mp[1] - p.y)*p.z*0.0005)

        return p

    def setPixel(self, a):
        
        x=int(round(a.x))
        y=int(round(a.y))
        z=int(round(a.z))
        color = (300-z, 300-z, 300-z)
        if self.zBuffer[x][y] > z:
            self.zBuffer[x][y] = z
            self.drawer.point((x, y), fill=color)


    def drawLine(self, p1, p2):

        longest_axis = (max(abs(p2.x - p1.x), abs(p2.y - p1.y)))
        
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

        spanLengthV3 = abs(p1.y - p3.y)
        spanLengthV2 = abs(p1.y - p2.y)

        t=0
        if (p2.y-p3.y) != 0:

            t = abs((p1.y-p3.y)/(p2.y-p3.y))

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
# color1 = (randint(0, rgb), randint(0,rgb), randint(0,rgb))
# color2 = (randint(0, rgb), randint(0,rgb), randint(0,rgb))
# color3 = (randint(0, rgb), randint(0,rgb), randint(0,rgb))
# color4 = (25, 90, 100)

hjul1 = [0,600,0]
hjul2 = [400,600,00]
hjul3 = [0,600,100]
hjul4 = [400,600,100]

vTranslate =[0, -200, 0]

mScale = [0.25, 0.25, 0.25]

loadedObject = Obj("cylinder")
cube = Model(loadedObject.points, loadedObject.edges, loadedObject.triangles)
screen.drawModel(cube, hjul1, mScale, vTranslate, False)
screen.drawModel(cube, hjul2, mScale, vTranslate, False)
screen.drawModel(cube, hjul3, mScale, vTranslate, False)
screen.drawModel(cube, hjul4, mScale, vTranslate, False)
# mTranslate = [0,0,0]
# loadedObject = Obj("Kub")
# cube = Model(loadedObject.points, loadedObject.edges, loadedObject.triangles)
# screen.drawModel(cube, mTranslate, mScale, vTranslate, False)

# loadedObject = Obj("cylinder")
# cube = Model(loadedObject.points, loadedObject.edges, loadedObject.triangles)
# screen.drawModel(cube, mTranslate, mScale, vTranslate, False)

# loadedObject = Obj("hjul2")
# cube = Model(loadedObject.points, loadedObject.edges, loadedObject.triangles)
# screen.drawModel(cube, True)

screen.saveImage("beautiful")

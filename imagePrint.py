from PIL import Image, ImageDraw


class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
     
    def lerp(a, b, t):
        return Point(Math.flerp(a.x, b.x, t), Math.flerp(a.y, b.y, t), Math.lerpColors(a.color, b.color, t))

class Math:

    def flerp(a, b, t):
        x = a + (b - a)*t
        return x

    def lerpColors(col1, col2, t):
        x = []
        for i in range(0,3):
            y=Math.flerp(col1[i], col2[i], t)
            x.append(y)
        z = (int(round(x[0])),int(round(x[1])), int(round(x[2])))
        return z

    def lerpVect(v1, v2, length):
        a = int(round(v1[0] + (v2[0]-v1[0])*length))
        b = int(round(v1[1] + (v2[1]-v1[1])*length))
        v = [a,b]
        return v

    def sortVec(v1, v2, v3):
        x = [v1[1],v2[1],v3[1]]
        x = sorted(x)

        if v2[1] == x[1]:
            temp=v1
            v1=v2
            v2=temp

        if v3[1] == x[1]:
            temp=v1
            v1=v3
            v3=temp
        if v2[1] == x[0]:
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
 
    def setPixel(self, x, y, color):
        self.drawer.point((x, y), fill=color)

    def drawLine(self, point1, point2, color1, color2):
        xLength = point1[0] - point2[0]
        yLength = point1[1] - point2[1]
        xLength = abs(xLength)

        yLength = abs(yLength)

        maxLength = max(xLength, yLength)
        xParam = 1
        yParam = 1
        xRatio = 1
        yRatio = 1
        if point1[0] > point2[0]:
            xParam = -1
        if point1[1] > point2[1]:
            yParam = -1        

        if max(xLength, yLength) == yLength and yLength != xLength:
            xRatio=xLength/yLength
            yRatio=1

        if max(xLength, yLength) == xLength and xLength != yLength:
            xRatio=1
            yRatio=yLength/xLength
        x=[]
        y=[]


        for i in range (0, maxLength +1):
            x.append(point1[0] + xRatio*i * xParam)
            x[i]= int(round(x[i]))
            y.append(point1[1] + yRatio*i * yParam)
            y[i] = int(round(y[i]))
            if i != 0:
                z= i/maxLength
            else:
                z=0
            color = Math.lerpColors(color1, color2, z)
            #a=[x[i]] [y[i]]
            self.setPixel(x[i], y[i], color)
            
    def drawRectangle(x, y, width, height, col1, col2, col3, col4):
        topLineStart = [x, y]
        topLineEnd = [x, y + width - 1]

        for i in range (0, height):
            color1 = Math.lerpColors(col1, col3, i/height)
            color2 = Math.lerpColors(col2, col4, i/height)
            Math.drawLine(topLineStart, topLineEnd, color1, color2)
            topLineStart[0] += 1
            topLineEnd[0] += 1

    def drawTriangle(self, v1, v2, v3, color, color2, color3):
        #self.drawLine(v1, v2, symbol)
        #self.drawLine(v2, v3, symbol)
        #self.drawLine(v1, v3, symbol)
        v1, v2, v3 = Math.sortVec(v1, v2, v3)
        
        spanLengthV3 = abs(v1[1] - v3[1])
        spanLengthV2 = abs(v1[1] - v2[1])
        spanLength = abs(max(v1[0], v1[1]))
        if spanLengthV2 == 0:
            spanLengthV2 = 1
        if spanLengthV3 == 0:
            spanLengthV3 = 1
        #if max(xLength, yLength) == yLength and yLength != xLength:
       #     xRatio=xLength/yLength
        #    yRatio=1

        #if max(xLength, yLength) == xLength and xLength != yLength:
        #    xRatio=1
        #    yRatio=yLength/xLength
        t = abs((v1[1]-v3[1])/(v2[1]-v3[1]))
        v4 = Math.lerpVect(v3, v2, t)
        color4 = Math.lerpColors(color3, color2, t)
        print(color4)

        for i in range(0, spanLengthV2 + 1):
            a = Math.lerpVect(v2,v1, 1/spanLengthV2*i)
            b = Math.lerpVect(v2,v4, 1/spanLengthV2*i)
            col1 = Math.lerpColors(color2, color, 1/spanLengthV2*i)
            col2 = Math.lerpColors(color2, color4, 1/spanLengthV2*i)
            self.drawLine(a, b, col1, col2)

        for i in range(0, spanLengthV3 + 1):
            a = Math.lerpVect(v3,v1, 1/spanLengthV3*i)
            b = Math.lerpVect(v3,v4, 1/spanLengthV3*i)
            col3 = Math.lerpColors(color3, color, 1/spanLengthV3*i)
            col4 = Math.lerpColors(color3, color4, 1/spanLengthV3*i)
            self.drawLine(a, b, col3, col4)

#    def draw(self):
 #       print("-"*self.width*2 + "-")
  #      string="|" + ('|\n|'.join(' '.join(str(cell) for cell in row) for row in self.a)) + "|"
   #     print(string)
    #    print("-"*self.width*2 + "-")

    def saveImage(self, name):
        self.backingImage.save(name + ".png")

screen = canvas(800, 600, " ")
v1 = [234, 400]
v2 = [125, 123]
v3 = [439, 400]

color1 = (255, 125, 79)
color2 = (14, 255, 124)
color3 = (67, 28, 255)
color4 = (25, 90, 100)


p1 = Point(245, 576, color1)
p2 = Point(462, 124, color2)
p3 = Point(412, 241, color3)
#p3 = Point.lerp(p1, p2, 0.5)
#drawLine(p2, p3)
screen.drawTriangle(v1, v2, v3, color1, color2, color3)
#screen.drawTriangle(v1, v2, v3, color1, color2, color3)
#screen.drawLine(v1, v2, color1, color1)
#screen.drawLine(v1, v3, color1, color1)
#screen.drawLine(v2, v3, color1, color1)
width = 800
height = 600
#screen.drawRectangle(v1[0], v1[1], height, width, color1, color2, color3, color4)
screen.saveImage("beautiful")
#screen.draw()
from PIL import Image, ImageDraw

class canvas:
    def __init__(self, width, height, filler):
        self.width = width
        self.height = height
        self.a = [[filler for i in range(self.width)] for j in range(self.height)]
        self.filler = filler
        size = [width, height]
        self.im =Image.new('RGB', size, (255, 255, 255))

 
    def setPixel(self, b, c, symbol2):
        self.a[b][c] = symbol2
    
    
    def drawLine(self, point1, point2, color):
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
        pix = self.im.load()

        for i in range (0, maxLength +1):
            x.append(point1[0] + xRatio*i * xParam)
            x[i]= int(round(x[i]))
            y.append(point1[1] + yRatio*i * yParam)
            y[i] = int(round(y[i]))

        for i in range (0, maxLength):

            pix[x[i], y[i]] = color
        self.saveImage()

    def drawRectangle(self, x, y, width, height, symbol):
        topLineStart = [x, y]
        topLineEnd = [x, y + width - 1]

        for i in range (0, height):
            self.drawLine(topLineStart, topLineEnd, symbol)
            topLineStart[0] += 1
            topLineEnd[0] += 1

    def lerp(self, v1, v2, length):
        a = v2[0]-v1[0]
        b = v2[1]-v1[1]
        v = [int(round(a*length)), int(round(b*length))]
        return v

    def sortVec(self, v1, v2, v3):
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

    def drawTriangle(self, v1, v2, v3, symbol):
        #self.drawLine(v1, v2, symbol)
        #self.drawLine(v2, v3, symbol)
        #self.drawLine(v1, v3, symbol)
        v1, v2, v3 = self.sortVec(v1, v2, v3)
        spanLengthV3 = abs(v1[1] - v3[1])
        spanLengthV2 = abs(v1[1] - v2[1])
        spanLength = abs(max(v1[0], v1[1]))

        #if max(xLength, yLength) == yLength and yLength != xLength:
       #     xRatio=xLength/yLength
        #    yRatio=1

        #if max(xLength, yLength) == xLength and xLength != yLength:
        #    xRatio=1
        #    yRatio=yLength/xLength
        t = abs((v1[1]-v3[1])/(v2[1]-v3[1]))
        v4 = self.lerp(v2, v3, t)
        v4[0] = v4[0] + v2[0]



        for i in range(0, spanLengthV2 + 1):
            a = self.lerp(v2,v1, 1/spanLengthV2*i)
            b = self.lerp(v2,v4, 1/spanLengthV2*i)

            a[0] = a[0] + v2[0]
            a[1] = a[1] + v2[1]
            b[0] = b[0] + v2[0]
            b[1] = b[1] + v2[1]

            self.drawLine(a, b, symbol)

        for i in range(0, spanLengthV3 + 1):
            a = self.lerp(v3,v1, 1/spanLengthV3*i)
            b = self.lerp(v3,v4, 1/spanLengthV3*i)
            a[0] = a[0] + v3[0]
            a[1] = a[1] + v3[1]
            b[0] = b[0] + v3[0]
            b[1] = b[1] + v3[1]

            self.drawLine(a, b, symbol)

        #for i in range(0, spanLength):
        #    a = self.lerp(v1,v3, 1/spanLength*i)
        #    b = self.lerp(v1,v4, 1/spanLength*i)
        #    a[0] = a[0] + v1[0]
       #     a[1] = a[1] + v1[1]
       #     b[0] = b[0] + v1[0]
      #      b[1] = b[1] + v1[1]
      #      self.drawLine(a, b, symbol)

    def draw(self):
        print("-"*self.width*2 + "-")
        string="|" + ('|\n|'.join(' '.join(str(cell) for cell in row) for row in self.a)) + "|"
        print(string)
        print("-"*self.width*2 + "-")

    def saveImage(self):
        self.im.save("beautiful.png")

screen = canvas(30, 30, " ")
v1 = [10, 16]
v2 = [12, 2]
#v3 = [6, 16]
#screen.drawTriangle(v1, v2, v3, "*")
color = (130, 230, 15)
screen.drawLine(v1, v2, color)

#screen.draw()
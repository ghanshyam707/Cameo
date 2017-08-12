import cv2;
import numpy;
import utils;
import rects

class Face(object):
    def __init__(self):
        self.face = None
        self.nose = None
        self.lefteye = None
        self.righteye = None
        self.smile = None
            
class FaceDetect(object):
    def __init__ (self,scale = 1.2,neighbour = 2,flag = cv2.CASCADE_SCALE_IMAGE):
        self.scale = scale
        self.neighbour = neighbour
        self.flag = flag
        self.faces = []
        self.swapfaces = []
        self.facedetector = cv2.CascadeClassifier("cascades/haarcascade_frontalface_alt2.xml")
        self.lefteyedetector = cv2.CascadeClassifier("cascades/haarcascade_lefteye_2splits.xml")
        self.smiledetector = cv2.CascadeClassifier("cascades/haarcascade_smile.xml")
        self.righteyedetector = cv2.CascadeClassifier("cascades/haarcascade_righteye_2splits.xml")

    def getFaces (self):
        return self.swapfaces

    def  detectObject(self,classifier,image,rect,imageratio):
        minscale = utils.divideHeightWidth(image,imageratio)
        x,y,w,h = rect
        img = image[y:y+h,x:x+w]
        results = classifier.detectMultiScale(img,self.scale,self.neighbour,self.flag,minscale)
        if len(results) > 0 :
            result = results[0]
            dx,dy,dw,dh = result
            return(x+dx,y+dy,dw,dh)
        else:
            return None
            

    def update (self,image):
        self.swapfaces = []
        if utils.isGray(image):
            cv2.equalizeHist(image,image)
        else:
            image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            cv2.equalizeHist(image,image)
        minscale = utils.divideHeightWidth(image,8)
        facerects = self.facedetector.detectMultiScale(image,self.scale,self.neighbour,self.flag,minscale)
        facearea = Face()
        self.swapfaces.append(facerects)
        if len(facerects)  > 0:
            for face in facerects :
                facearea.face = face
                x,y,w,h = face
                searcharea = (x+w/7,y,w*2/7,h/2)
                facearea.lefteye = FaceDetect.detectObject(self,self.lefteyedetector,image,searcharea,64)
                searcharea = (x+w*4/7,y,w*2/7,h/2)
                facearea.righteye = FaceDetect.detectObject(self,self.righteyedetector,image,searcharea,64)
                #searcharea = (x+w/4,y+h/4,w/2,h/2)
                #facearea.nose = detectObject(self.nosedetector,image,searcharea,32)
                searcharea = (x+w/3,y+h*2/3,w*2/3,h/3)
                facearea.smile = FaceDetect.detectObject(self,self.smiledetector,image,searcharea,16)
                self.faces.append(facearea)
        

    def  drawRect (self,image):
        if utils.isGray(image):
            faceColor = 255
            leftEyeColor = 255
            rightEyeColor = 255
            noseColor = 255
            mouthColor = 255
        else:
            faceColor = (255, 255, 255) # white
            leftEyeColor = (0, 0, 255) # red
            rightEyeColor = (0, 255, 255) # yellow
            #noseColor = (0, 255, 0) # green
            mouthColor = (255, 0, 0) # blue
        for face in self.faces:
            rects.outlineRect(image, faceColor, face.face)
            rects.outlineRect(image, leftEyeColor, face.lefteye)
            rects.outlineRect(image,rightEyeColor, face.righteye)
            #rects.outlineRect(image, face.noseRect, noseColor)
            rects.outlineRect(image, mouthColor, face.smile)
            self.faces = []
        

        

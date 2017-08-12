import cv2
import time
import numpy

class CaptureManager (object):

    def __init__(self,channel=0,videowriter = None,windowmanager = None,ismirrorpreview = False):
        self.channel = channel
        self.videocapture = cv2.VideoCapture(self.channel)
        self.presentframe = None
        self.previousframeexist = False
        self .videofilename = None
        self.imagefilename = None
        self.videowriter = videowriter
        self.windowmanager = windowmanager
        self.ismirrorpreview = ismirrorpreview
        self.videoencoder = None
        self.frameelapsed = 0
        self.starttime = 0
        self.estimatedfps = 0

    def enterframe (self):
        assert not self.previousframeexist ,\
               'privious frame in process'
        if not self.previousframeexist and self.videocapture is not None:
            if self.videocapture.grab():
                success,self.presentframe = self.videocapture.retrieve(self.channel)
        if success :
            self.previousframeexist = True

    def getFrame (self):
        return self.presentframe

    def exitframe (self):
        if not self.previousframeexist:
            return
        if self.frameelapsed == 0:
            self.starttime = time.time()
        else:
            self.estimatedfps = self.frameelapsed/(time.time()-self.starttime)
        self.frameelapsed += 1
        if self.windowmanager is not None:
            if self.ismirrorpreview:
                frame = numpy.fliplr(self.presentframe).copy()
                self.windowmanager.show(frame)
                #cv2.imshow('window',self.presentframe)
            else:
                self.windowmanager.show(self.presentframe)
                #cv2.imshow('window',self.presentframe)
        self.writevideoframe()
        self.presentframe = None
        self.previousframeexist = False
        
    def writevideoframe (self):
        if self.videofilename is not None:
            if self.videowriter is  None:
                #fps =  self.videocapture.get(2)
                fps = 0
                if fps == 0:
                    if self.frameelapsed < 20:
                        return
                    fps = self.estimatedfps
                size = (int (self.videocapture.get(3)),int(self.videocapture.get(4)))
                self.videowriter = cv2.VideoWriter(self.videofilename,self.videoencoder,fps,size)
            self.videowriter.write(self.presentframe)

    def writeimage (self):
        if self.presentframe is not None:
            print('true')
        else:
            print('false')
        if self.imagefilename is not None:
            cv2.imwrite(self.imagefilename,self.presentframe)

    def startvideowriting (self,videofilename,videoencoder = None):
        self.videofilename = videofilename
        if videoencoder is not None:
            self.videoencoder = videoencoder
        else:
            self.videoencoder = cv2.VideoWriter_fourcc('I','4','2','0')
        self.writevideoframe()
        
    def captureimage (self,imagefilename):
        self.imagefilename = imagefilename
        self.writeimage()

    def stopvideowriting (self):
        self.videofilename = None
        self.videoencoder = None
        self.videowriter = None

    def isvideowriting (self):
        return self.videofilename is not None


class WindowManager (object):

    def __init__(self,windowname = None,onkeypresscallback = None):
        self.windowname = windowname
        self.windowcreated  = False
        self.onkeypresscallback = onkeypresscallback

    def  createwindow (self):
        cv2.namedWindow(self.windowname)
        self.windowcreated = True

    def  show (self,frame):
        cv2.imshow(self.windowname,frame)

    def destroywindow (self):
        cv2.destroyWindow(self.windowname)
        self.windowcreated = False

    def iswindowcreated (self): 
        return self.windowcreated

    def processevent (self):
        key = cv2.waitKey(1)
        if key != -1:
            key &= 0xFF
        self.onkeypresscallback(key)

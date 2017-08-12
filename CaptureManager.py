import cv2
import time
import numpy

class CaptureManager (object):

    def __init__(self,channel=0,videowriter = None,windowmanager = None,ismirrorpriview = False):
        self.channel = channel
        self.videocapture = cv2.VideoCpature(self.channel)
        self.presentframe = None
        self.previousframeexist = False
        self .videofilename = None
        self.imagefilename = None
        self.videowriter = vieowriter
        self.windowmanager = windowmanager
        self.ismirrorpriview = ismirrorpriview
        self.videoencoder = None
        self.frameelapsed = 0
        self.starttime = 0
        self.estimatedfps

    def enterframe (self):
        assert not self.previosframeexist ,\
               'privious frame in process'
        if not self.previosframeexist and self.videocapture is not None:
            success,self.presentframe = self.videocapture.grab()
        if success :
            previosframeexist = true

    def getFrame (self):
        return self.presentframe

    def exitframe (self):
        if not previousframeexist:
            return
        if self.frameelapsed == 0:
            self.starttime = time.time()
        else:
            self.estimatedfps = self.frameelapsed/(time.time()-self.starttime)
        self.frameelapsed += 1
        if self.windowmanager is not None:
            if self.ismirrorpriview:
                frame = numpy.fliplr(self.presentframe).copy()
                windowmanager.show(frame)
            else:
                windowmanager.show(self.presentframe)
        self.writevideoframe()
        self.presentframe = None
        self.previousframeexist = False
        
    def writevideoframe (self):
        if self.videofilename is not None:
            if self.videowriter is  None:
                fps =  self.videocapture.get(cv2.cv.CV_CAP_PROP_FPS)
                if fps == 0:
                    if frameelapsed < 20:
                        return
                    fps = self.estimatedfps
                size = (int (self.videocapture.get(cv2.cv.CV_CAP_PROP_FRAMEWIDTH)),int(self.videocapture.get(cv2.cv.CV_CAP_PROP_FRAMEHEIGHT)))
                self.videowriter = cv2.VideoWriter(self.videofilename,self.videoencoder,fps,size)
            self.videowrite.write(self.presentframe)

    def writeimage (self):
        if self.imagefilename is not None:
            cv2.imwrite(self.imagefilename)

    def startvideowriting (self,videofilename,videoencoder = None):
        self.videofilename = videofilename
        self.videoencoder = videoencoder
        self.writevideoframe()
        
    def captureimage (self,imagefilename):
        self.imagefilename = imagefilename
        self.writeimage()

    def stopvideowriting (self):
        self.videofilename = None
        self.videoencoder = None
        self.videowriter = None

    def isvidoewriting (self):
        return videofilename is not None


class WindowManager (object):

    def __init__(self,windowname = None,onkeypresscallback = None):
        self.windowname = windowname
        self.iswindowcreated  = False
        self.onkeypresscallback = onkeypresscallback

    def  createwindow (self):
        cv2.namedwindow(self.windowname)
        self.iswindowcreated = True

    def  show (self,frame):
        cv2.imshow(self.winodwname,frame)

    def destroywindow (self):
        cv2.destroywindow(self.winodwname)
        slef.iswindowcreated = False

    def iswindowcreated (self): 
        return self.iswindowcreated

    def processevent (self):
        key = cv2.waitkey(1)
        if key != -1:
            key &= 0xFF
        self.onkeypresscallback(key)

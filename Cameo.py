import cv2
from Managers import  CaptureManager,WindowManager
import filters
from tracker import FaceDetect
import rects
class Cameo(object):

    def __init__ (self):
        self._windowManager = WindowManager('Cameo',self.eventhandler)
        self._captureManager = CaptureManager(windowmanager = self._windowManager,ismirrorpreview = True)
        self._curveFilter = filters.BGRCrossProcess()
        self._kernelFilter = filters.AbossEffect()
        self._shrpenimage = filters.SharpenFilter()
        self._facetracker = FaceDetect()
    def run (self):
        self._windowManager.createwindow()
        while self._windowManager.iswindowcreated():
            self._captureManager.enterframe()
            frame = self._captureManager.getFrame()
            #filters.edgeStrock(frame,frame)
            #self._shrpenimage.apply(frame,frame)
            #self._kernelFilter.apply(frame,frame)
            self._curveFilter.apply(frame,frame)
            self._facetracker.update(frame)
            faces = self._facetracker.getFaces()
            rects.swapRect(frame,faces)
            self._facetracker.drawRect(frame)
            self._windowManager.processevent()
            self._captureManager.exitframe()


    def eventhandler (self,key):

        if key == 32:
            self._captureManager.captureimage('screenshot.png')
        elif key == 9:
            if self._captureManager.isvideowriting():
                self._captureManager.stopvideowriting()
            else:
                self._captureManager.startvideowriting('film.avi')
        elif key == 27:
            self._windowManager.destroywindow()

if  __name__ == "__main__":
    Cameo().run()

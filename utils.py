import cv2
import numpy
import scipy.interpolate

def createCurveFunc (points):
    if points is None:
        return None
    numPoints = len (points)
    if numPoints < 2 :
        return None
    if numPoints < 4 :
        type = 'linear'
    else :
        type = 'cubic'
    xs , ys = zip(*points)
    return scipy.interpolate.interp1d(xs , ys , type , bounds_error  = False)

def createLookUpTable (function , length = 255):
    if function is None:
        return None
    lookUpTable = numpy.empty(length+1)
    i = 0
    while i < length:
        value = function(i)
        lookUpTable[i] = min (max(value,0),length)
        i += 1
    return lookUpTable
def applyLookUpTable (table,src,des):
    if table is None:
        return
    des[:] =  table[src]
            
def createCompositeFunction (func1,func2):
    if func1 is None:
        return None
    if func2 is None:
        return None
    return lambda x : func2(func1(x))

def createFlatView (array):
    return array.view()

def isGray (img):
    return img.ndim < 3

def divideHeightWidth(img,divisor):
    h,w = img.shape[:2]
    return(int(h/divisor),int(w/divisor))

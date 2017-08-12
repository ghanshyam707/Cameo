import cv2
import utils
import numpy

class VFuncFilters (object):

    def __init__ (self,vFuncution , dtype) :
        length = numpy.iinfo(dtype).max
        self.lookUpTable = utils.createLookUpTable(vFuncution , length)

    def apply (self,src,dest):
        srcFlateView = utils.createLookUpTable(src)
        destFlatView = utils.createLookUpTable(dest)
        utils.applyLookUpTable(self.lookUpTable,srcFlateView,destFlatView)

class VCurveFilter (VFuncFilters):

    def __init__ (self,points,dtype = numpy.uint8):
        VFuncFilters(utils.createCurveFunc(points),dtype)

class BGRFuncFilter (object):

    def __init__(self,vfunc,rfunc,gfunc,bfunc,dtype):
        length = numpy.iinfo(dtype).max
        self.rlookUptable = utils.createLookUpTable(utils.createCompositeFunction(vfunc,rfunc),length)
        self.glookUptable = utils.createLookUpTable(utils.createCompositeFunction(vfunc,gfunc),length)
        self.blookUptable = utils.createLookUpTable(utils.createCompositeFunction(vfunc,bfunc),length)

    def apply (self,src,dest):
        r,g,b = cv2.split(src)
        utils.applyLookUpTable(self.rlookUptable,r,r)
        utils.applyLookUpTable(self.glookUptable,g,g)
        utils.applyLookUpTable(self.blookUptable,b,b)
        cv2.merge([r,g,b],dest)

class BGRCurveFilter (BGRFuncFilter):

    def __init__ (self,vpoints=None,rpoints=None,gpoints=None,bpoints=None,dtype = numpy.uint8):
        BGRFuncFilter.__init__(self,
                               utils.createCurveFunc(vpoints),
                               utils.createCurveFunc(rpoints),
                               utils.createCurveFunc(gpoints),
                               utils.createCurveFunc(bpoints),dtype)

class BGRPortraCurveFilter(BGRCurveFilter):

    def __init__ (self,dtype = numpy.uint8):
        BGRCurveFilter.__init__(self,
                        vpoints = [(0,0) , (23,20) , (157,173) , (255,255)],
                       bpoints = [(0,0) , (41,46) , (231,228) , (255,255)],
                       gpoints = [(0,0) , (52,47) , (189,196) , (255,255)],
                       rpoints = [(0,0) , (69,69) , (213,218) , (255,255)],
                       dtype = dtype)

class BGRCrossProcess(BGRCurveFilter):

    def __init__ (self,dtype = numpy.uint8):
        BGRCurveFilter.__init__(self,
                       bpoints = [(0,20) ,  (255,235)],
                       gpoints = [(0,0) , (56,39) , (208,226) , (255,255)],
                       rpoints = [(0,0) , (56,22) , (211,255) , (255,255)],
                       dtype = dtype)

class KernelFilter (object):
    def __init__ (self,kernel):
        self.kernel = kernel
    def apply (self,src,dest):
        cv2.filter2D(src, -1,self.kernel,dest)

class AbossEffect (KernelFilter):
    def __init__ (self):
        kernel = numpy.array([[-2,-1,0],
                                                      [-1,1,1],
                                                      [0,1,2]])
        KernelFilter.__init__(self,kernel)

class SharpenFilter (KernelFilter):
    def __init__(self):
        kernel = numpy.array([[-1, -1, -1],
                                                    [-1, 9, -1],
                                                    [-1, -1, -1]])
        KernelFilter.__init__(self,kernel)
        
def edgeStrock (src,dest,kstrock = 7, estrock = 5):

    if kstrock > 3:
        blurredsrc = cv2.medianBlur(src,kstrock)
        graysrc = cv2.cvtColor(blurredsrc,cv2.COLOR_BGR2GRAY)
    else:
        graysrc = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
    cv2.Laplacian(graysrc,cv2.CV_8U,graysrc,estrock)
    normalizedinversealpha = (1.0/255)*(255-graysrc)
    channels = cv2.split(src)
    for channel in channels:
        channel[:] = normalizedinversealpha*channel
    cv2.merge(channels,dest)
        
    

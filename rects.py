import cv2
import numpy


def outlineRect (img,color,rect = None):
    if rect is not None:
        x,y,w,h = rect
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)
        cv2.rectangle(img,(x,y),(x+w,y+h),color)

def swapRect(img,rects,interpolation = cv2.INTER_LINEAR):
    if rects is None:
        return
    totalrects = len(rects)
    if totalrects < 2:
        return
    print("two faces detected")
    x,y,w,h = rects[0]
    dx,dy,dw,dh = rects[totalrects-1]
    src[:] = img[dy:dy+dh,dx:dx+dw].deepCopy()
    i = 0
    while i < totalrects - 1:
        copyrects(img,rects[i],rects[i+1],interpolation)
    img[y:y+h,x:x+h] = cv2.resize(src,(w,h),interpolation)

def copyRects (img,srcrect,destrect,interpolation):
    if srcrect is not None and destrect is not None:
        x,y,w,h = srcrect
        dx,dy,dw,dh = destrect

        img[dy:dy+dh,dx:dx+dw] =  cv2.resize(destrect,(w,h),interpolation)
    

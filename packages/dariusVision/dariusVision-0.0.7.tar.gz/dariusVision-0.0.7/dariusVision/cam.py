#가장 마지막(최신) 프레임을 얻어오는 카메라 모듈 
#%%
import cv2 as cv 
import sys
import time 
import numpy as np
import threading



# print(cv.__version__)
class lastest_Cam2 :
    def __init__(self,vid_src,grab_delay=0.1,width=640,height=480,bShow=False,onUpdate=None) :
        
        self.running = False #thread running flag
        self.vid_src = vid_src
        self.width = width
        self.height = height
        
        self.grab_delay = grab_delay
        self.frame_status = False
        self.bShow = bShow
        self.onUpdate = onUpdate
    
    def isOpened(self):
        return self.frame_status
    
    def _appLoop(self) :
        print('cam thread start')
        # cap = self.cap
        #프레임을 항상 최신으로 유지한다.
        while self.running:
            
            if self.bPause == False :
                with self._critical_Section :
                    ret,frame = self.cap.read()
                    self.frame_status = ret
                    if ret:
                        self.frame = frame
                        if self.onUpdate :
                            self.onUpdate(frame)
            time.sleep(self.grab_delay)
        
        self.cap.release()
        print('capture v2 thread end')
    
    def reconnect(self,vid_src) :
        self.bPause = True
        self.cap.release()
        self.cap = cv.VideoCapture(vid_src)
        self.bPause = False
        

    def read(self) :
        with self._critical_Section :
            return self.frame_status,self.frame.copy()
        
    def getFrame(self) :
        if self.running == True :
            status,frame = self.read()
            return status,None,frame
        else :
            return self.running,None,self.cap.read()
        
    def startCamera(self) :
        self.cap = cv.VideoCapture(self.vid_src)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.height)  
        
        if self.cap.isOpened():
            # print(cap)
            print(f'cam ok  {self.width}:{self.height}')
            ret,frame = self.cap.read()
            self.frame_status = ret
            self.frame = frame

        else :
            print('connect failed')
            
    def doLastFrame(self) :
        self.running = True
        self.bPause = False
        self._critical_Section = threading.Lock()
        t = threading.Thread(target=self._appLoop)
        #주쓰레가 죽으면 같으죽는다. FALSE이면 주쓰레드와 관계없이 계속 동작한다.
        t.daemon = True
        t.start()
        self.threadObj = t
        
    def stopCamera(self) :
        if self.running == True :
            self.running = False
        else :
            self.cap.release()
#%% start thread
if __name__== '__main__':

    import PIL.Image as Image
    import PIL.ImageColor as ImageColor
    import PIL.ImageDraw as ImageDraw
    import PIL.ImageFont as ImageFont

    from IPython.display import display
    # app = QApplication(sys.argv)
    app = lastest_Cam2(vid_src='rtsp://admin:71021@192.168.4.19/stream_ch00_0')
    _ ,frame = app.getframe()
    if _ == True :
        _img = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        display(Image.fromarray(_img))
    else:
        print('capture failed')

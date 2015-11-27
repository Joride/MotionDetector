
import time
from datetime import datetime

# time = datetime.now()
# filename = "capture-%04d%02d%02d-%02d%02d%02d.bmp" % (time.year, time.month, time.day, time.hour, time.minute, time.second)
# output = "/home/pi/motiondetection/%s" % filename






# process an image
# from PIL import Image
# image = Image.open(output)
# pixelData = image.load()

# imageSize = image.size
# x = imageSize[0]
# y = imageSize[1]
# print image.size
# print "y = %s" % y
# print "x = %s" % x

# inspect each pixel's values
# for xPixel in range(0, x):    
#     for yPixel in range(0, y):
#         print pixelData[xPixel,yPixel]


######
#
#
from threading import Timer
import picamera
class PiCameraSnapshotter():
    delegate = None
    _isSnapshotting = False
    _camera = None
    def __init__(
        self,
        repeats = False,
        interval = 1):
        
        self.repeats = repeats
        self.interval = interval
     
    def _timerFired(self):
        if self._isSnapshotting == True:
            if self._camera == None:
                # instantiate the piCamera object, set some values
                self._camera = picamera.PiCamera()
                self._camera.brightness = 50
                self._camera.rotation = 270 # valid values are: 0, 90, 180,  270

            # tell the camera to take a picture
            imageSize = (240, 135,)#(1920, 1080)
            fileName = self.delegate.fileName()
            self._camera.capture(
                fileName,
                format='bmp',
                use_video_port=False,
                resize=imageSize,
                splitter_port=0,)
        else:
            print "Timer fired but not taking a snapshot, because because stopSnapShotting() was called before the timer fired."
    
        if self.repeats and self._isSnapshotting == True:
            thread = Timer(self.interval, self._timerFired, args=[])        
            thread.start()
        else:
            print "Timer fired, but not starting a new timer, because because stopSnapShotting() was called while we were taking a snapshot."

    def startSnapShotting(self):
        if self._isSnapshotting == False:
            self._isSnapshotting = True
            thread = Timer(self.interval, self._timerFired, args=[])
            thread.start()

    def stopSnapShotting(self):
        if self._isSnapshotting == True:
            self._isSnapshotting = False
            self._camera = None


import time
class MotionDetector():
    def fileName(self):
        fileName = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        fileName = "%s.bmp" % fileName
        return fileName
 
    def startDetecting(self):
        snapShotter = PiCameraSnapshotter(repeats = True, interval = 1.0)
        snapShotter.delegate = self
 
        snapShotter.startSnapShotting()
        time.sleep(10)
        snapShotter.stopSnapShotting()

detector = MotionDetector()
detector.startDetecting()





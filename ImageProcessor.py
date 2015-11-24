import picamera
import time
from datetime import datetime

time = datetime.now()
filename = "capture-%04d%02d%02d-%02d%02d%02d.bmp" % (time.year, time.month, time.day, time.hour, time.minute, time.second)
output = "/home/pi/motiondetection/%s" % filename

# instantiate the piCamera object, set some values
camera = picamera.PiCamera()
camera.framerate = 30
camera.brightness = 50
camera.rotation = 270 # valid values are: 0, 90, 180,  270

# tell the camera to take a picture
imageSize = (240, 135,)#(1920, 1080)
camera.capture(output, format='bmp', use_video_port=False, resize=imageSize, splitter_port=0,)


# process an image
from PIL import Image
image = Image.open(output)
pixelData = image.load()

imageSize = image.size
x = imageSize[0]
y = imageSize[1]
print image.size
print "y = %s" % y
print "x = %s" % x

# inspect each pixel's values
# for xPixel in range(0, x):    
#     for yPixel in range(0, y):
#         print pixelData[xPixel,yPixel]


######
#
#
from threading import Timer
class PiCameraSnapshotter():
    delegate = None
    _isSnapshotting = False
    def __init__(
        self,
        repeats = False,
        interval = 0):
        self.repeats = repeats
        self.interval = interval
        self.thread = Timer(interval, self._timerFired, args=[])
     
    def _timerFired(self):
        if self.repeats:
            fileName = self.delegate.fileName()
            print "fileName: %s" % fileName
            self.thread = Timer(self.interval, self._timerFired, args=[])        
            self.thread.start()

    def startSnapShotting(self):
        if self._isSnapshotting != True:
            self._isSnapshotting = True
            self.thread.start()

    def stopSnapShotting(self):
        if self._isSnapshotting == True:
            self._isSnapshotting = False
            self.thread.cancel()


import time
class MotionDetector():
    def fileName(self):
        fileName = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        return fileName
 
    def startDetecting(self):
        snapShotter = PiCameraSnapshotter(repeats = True, interval = 0.5)
        snapShotter.delegate = self

        print "starting to snapshot %s" % datetime.now().second
        snapShotter.startSnapShotting()
        time.sleep(10)
        print "stopping snapshotting %s" % datetime.now().second
        snapShotter.stopSnapShotting()

detector = MotionDetector()
detector.startDetecting()





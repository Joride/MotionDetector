from PIL import Image
class ImageAnalyzer():
    _isCancelled = False
    _singlePixelThreshold = 0
    def __init__(self, singlePixelThreshold = 15):
        self._singlePixelThreshold = singlePixelThreshold


    def compareImages(self, imagePath1, imagePath2):
        # process an image

        image1 = Image.open(imagePath1)
        imageSize1= image1.size
        x1 = imageSize1[0]
        y1 = imageSize1[1]
        print image1.size

        image2 = Image.open(imagePath2)
        imageSize2= image2.size
        x2 = imageSize2[0]
        y2 = imageSize2[1]
        print image2.size

        totalNumberOfPixels = x2 * y2
        if not ((x2 is x1) and (y2 is y1)):
            print "Images of different sizes cannot be compared"
        else:
            pixelData1 = image1.load()
            pixelData2 = image2.load()

            differentPixelCount = 0
            totalSquaredDifference = 0
            
            # compare each pixel's values
            for xPixel in range(0, x1):
                if self._isCancelled == True:
                    break
                for yPixel in range(0, y1):
                    if self._isCancelled == True:
                        break

                    # values range from 0 - 255
                    (r1,g1,b1) = pixelData1[xPixel,yPixel]
                    (r2,g2,b2) = pixelData2[xPixel,yPixel]
                    
                    difference = abs(g1 - g2)
                    if difference > self._singlePixelThreshold:
                        differentPixelCount += 1
                        totalSquaredDifference += difference
                    
            if self._isCancelled:
                return None
            else:
                return (differentPixelCount, totalSquaredDifference, totalNumberOfPixels)
    
    def cancel(self):
        self._isCancelled = True


import time
from datetime import datetime
from threading import Thread
from PiCameraSnapshotter import PiCameraSnapshotter

class MotionDetector():
    _snapShotter = None
    _isDetecting = False
    _imageAnalyzer = None
    _previousImagePath = None

    # PiCameraSnapShotter callbacks
    def snapShotterFileNameForCapture(self):
        fileName = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        fileName = "%s.bmp" % fileName
        return fileName

    def snapShotterDidCaptureImage(self, snapShotter, imagePath):
        if self._previousImagePath == None:
            self._previousImagePath = imagePath
        else:
            if self._imageAnalyzer == None:
                self._imageAnalyzer = ImageAnalyzer()

            if imagePath is not None and self._previousImagePath is not None:
                analysisResult = self._imageAnalyzer.compareImages(imagePath, self._previousImagePath)
                if analysisResult != None:
                    (differentPixelCount,
                        totalSquaredDifference,
                        totalNumberOfPixels) = analysisResult
                    print "differentPixelCount: %s" % differentPixelCount
                    print "totalSquaredDifference: %s" % totalSquaredDifference
                    print "totalNumberOfPixels: %s" % totalNumberOfPixels

            self._previousImagePath = imagePath

        
 
    def startDetecting(self):
        if self._isDetecting == False:
            self._isDetecting = True
            thread = Thread(target = self._startDetectingOnThread)
            thread.start()
            
        else:
            print "Already detecting, ignoring call to startDetecting()"
    
    def _startDetectingOnThread(self):
        if self._snapShotter == None:
            snapShotter = PiCameraSnapshotter(repeats = True, interval = 1.0)
            snapShotter.delegate = self
 
        snapShotter.startSnapShotting()
        while self._isDetecting == True:
            time.sleep(1)

        snapShotter.stopSnapShotting()


    def stopDetecting(self):
        if self._isDetecting == True:
            self._imageAnalyzer.cancel();
            self._isDetecting = False
        else:
            print "Not detecting, ignoring call to stopDetecting()"

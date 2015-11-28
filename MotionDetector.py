from ImageAnalyzer import ImageAnalyzer

import time
from datetime import datetime
from threading import Thread
from PiCameraSnapshotter import PiCameraSnapshotter
import os

class MotionDetector():
    _snapShotter = None
    _isDetecting = False
    _imageAnalyzer = None

    # PiCameraSnapShotter callbacks
    def snapShotterFileNameForCapture(self):
        fileName = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        fileName = "%s.bmp" % fileName
        return fileName

    def snapShotterDidCaptureImage(self, snapShotter, imagePath):
        if self._imageAnalyzer == None:
            self._imageAnalyzer = ImageAnalyzer(initialImagePath = imagePath)
        else:
            analysisResult = self._imageAnalyzer.compareNextImage(
                imagePath)
            if analysisResult != None:
                (differentPixelCount,
                    totalSquaredDifference,
                    totalNumberOfPixels) = analysisResult
                print " "
                print "differentPixelCount: %s" % differentPixelCount
                print "totalSquaredDifference: %s" % totalSquaredDifference
                print "totalNumberOfPixels: %s" % totalNumberOfPixels
        os.remove(imagePath)

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

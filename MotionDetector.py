from ImageAnalyzer import ImageAnalyzer

import time
from datetime import datetime
from threading import Thread
from PiCameraSnapshotter import PiCameraSnapshotter
import os # to delete imagefiles

class MotionDetector():
    _hasIgnoredFirstImage = False
    _snapShotter = None
    _isDetecting = False
    _imageAnalyzer = None
    _previousPixelCounts = []
    _previousSquaredDifference = []
    numberOfImagesToAverage = 3


    # PiCameraSnapShotter callbacks
    def snapShotterFileNameForCapture(self):
        fileName = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        fileName = "%s.bmp" % fileName
        return fileName

    def snapShotterDidCaptureImage(self, snapShotter, imagePath):
        # the first image is ignored, as it is very different form the second
        # one, even when no change in the scene is present. (Maybe the PiCam
        # still has to focus or adjust light settings).
        if not self._hasIgnoredFirstImage:
            self._hasIgnoredFirstImage = True
            os.remove(imagePath)
            return

        if self._imageAnalyzer == None:
            self._imageAnalyzer = ImageAnalyzer(initialImagePath = imagePath)
        else:
            analysisResult = self._imageAnalyzer.compareNextImage(
                imagePath)
            if analysisResult != None:
                (differentPixelCount,
                    totalSquaredDifference,
                    totalNumberOfPixels) = analysisResult
                self.analyzeNewImageResult(
                    differentPixelCount,
                    totalSquaredDifference)

        os.remove(imagePath)

    def analyzeNewImageResult(
        self,
        differentPixelCount,
        totalSquaredDifference):

        self._previousPixelCounts.append(differentPixelCount)
        self._previousSquaredDifference.append(totalSquaredDifference)

        if len(self._previousSquaredDifference) > self.numberOfImagesToAverage:
            self._previousSquaredDifference.pop(0)
            self._previousPixelCounts.pop(0)

        if len(self._previousPixelCounts) == self.numberOfImagesToAverage:
            pixelSum = sum(self._previousSquaredDifference)
            pixelLength = len(self._previousSquaredDifference)
            averagePixelDifference = pixelSum / float(pixelLength)

            differenceSum = sum(self._previousPixelCounts)
            differenceLength = len(self._previousPixelCounts)
            averagePixelCount = differenceSum / float(differenceLength)

            pixels = abs(differentPixelCount - averagePixelCount)
            squaredDelta = None
            if abs(averagePixelDifference) > 0:
                squaredDelta = abs(totalSquaredDifference / averagePixelDifference)

            if squaredDelta > 1.1 and pixels > 10:
                print "MOTION DETECTED"

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

from PIL import Image
class ImageAnalyzer():
    _isCancelled = False
    _singlePixelThreshold = 0
    _previousImage = None
    _previousImageData = None

    def __init__(self,
        initialImagePath = None,
        singlePixelThreshold = 15):

        self._singlePixelThreshold = singlePixelThreshold
        self._previousImage = Image.open(initialImagePath)
        self._previousImageData = self._previousImage.load()

    def compareNextImage(self, imagePath):
        # process an image

        newImage = Image.open(imagePath)
        newImageSize= newImage.size
        x1 = newImageSize[0]
        y1 = newImageSize[1]

        previousImageSize = self._previousImage.size
        x2 = previousImageSize[0]
        y2 = previousImageSize[1]

        returnValue = None
        numberOfPixels = x2 * y2
        if not ((x2 is x1) and (y2 is y1)):
            print "Images of different sizes (%s and %s) cannot be compared" % (
                newImageSize,
                previousImageSize)
        else:
            newImageData = newImage.load()

            changedPixelsCount = 0
            totalSquaredDiff = 0

            # compare each pixel's values
            for xPixel in range(0, x1):
                if self._isCancelled == True:
                    break
                for yPixel in range(0, y1):
                    if self._isCancelled == True:
                        break

                    # values range from 0 - 255
                    (r1,g1,b1) = newImageData[xPixel,yPixel]
                    (r2,g2,b2) = self._previousImageData[xPixel,yPixel]

                    difference = abs(g1 - g2)
                    if difference > self._singlePixelThreshold:
                        changedPixelsCount += 1
                        totalSquaredDiff += difference

            if not self._isCancelled:
                returnValue = (
                    changedPixelsCount,
                    totalSquaredDiff,
                    numberOfPixels)

        self._previousImage = newImage
        self._previousImageData = newImageData

        return returnValue

    def cancel(self):
        self._isCancelled = True

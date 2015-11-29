from MotionDetector import MotionDetector # this class defines the callback that is implemented in this file

class MotionDectectorHandler():

    def motionDetectorDetectedMotion(self, motionDetector):
        print "MotionDectectorHandler motionDetectorDetectedMotion() called."
        print "This is where you call any code that should run in respons to motion."
        print "E.g. start to record video, send a push notification to a mobile device, etc."

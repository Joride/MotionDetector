# This file can be compared with Objective-C's main.m in which the
# UIApplicationMain() function sets up an infinite runloop.
#
# Here, the MotionDetector class sets up an infinite runloop when
# startDetecting() is called. In contrast to Objective-C's UIApplicationMain(),
# this mainLoop can be cancelled.

import sys # to catch the KeyboardInterrupt and SystemExit
from MotionDetection.MotionDetector import MotionDetector
from MotionDectectorHandler import MotionDectectorHandler

try:
    print "Type anything and hit <enter> to stop"
    handler = MotionDectectorHandler()
    detector = MotionDetector()
    detector.motionDetectorHandler = handler
    detector.startDetecting()
    input = raw_input()

    if input != None:
        detector.stopDetecting()

except (KeyboardInterrupt, SystemExit):
    detector.stopDetecting()


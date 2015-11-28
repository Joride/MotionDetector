import sys
from MotionDetector import MotionDetector
try:
    print "Type anything and hit <enter> to stop"
    detector = MotionDetector()
    detector.startDetecting()
    input = raw_input()
    
    if input != None:
        detector.stopDetecting() 

except (KeyboardInterrupt, SystemExit):
    detector.stopDetecting() 










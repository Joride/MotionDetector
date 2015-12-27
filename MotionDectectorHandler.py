from APNS.ApplePushNotification import ApplePushNotification
from APNS.ApplePushNotificationSender import ApplePushNotificationSender

class MotionDectectorHandler():

    def motionDetectorDetectedMotion(self, motionDetector):
        certfile = '/home/pi/certs/sPiView/aps_dev.pem'

        message = "Motion Detected"
        badgeCount = 0

        deviceTokens = (
        '49937176DCE4ABE88902659139C2DD940FDD3738484D73448FFF0712F2F5AC2A',
        )

        pushNotifications = []
        for aDeviceToken in deviceTokens:
            pn = ApplePushNotification()
            pn.deviceToken = aDeviceToken
            pn.message = message
            pushNotifications.append(pn)

        pnSender = ApplePushNotificationSender(certfile)
        pnSender.environment = 'sandbox'
        pnSender.pushNotifications = pushNotifications
        pnSender.sendPushNotifications()


        print "MotionDectectorHandler motionDetectorDetectedMotion() called."
        print "This is where you call any code that should run in respons to motion."
        print "E.g. start to record video, send a push notification to a mobile device, etc."

import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image, CompressedImage
from geometry_msgs.msg import Point
import cv2
import lib
import time

class Finder():
	def __init__(self):
		self.image_sub = rospy.Subscriber("/forward/image_raw", Image, self.image_callback, queue_size=1)
		self.bridge = CvBridge()
		self.image_pub = rospy.Publisher("/forward/processed", Image, queue_size=1)
	
	def image_callback(self, image_data):
		cv_image = self.bridge.imgmsg_to_cv2(image_data, "bgr8")
		t = time.time()
		rets, original_image = lib.find_pole(cv_image, draw=True)
		print "Time per frame: %2.4f" % (time.time() - t)

		if len(original_image.shape) == 2:
			original_image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)
		self.image_pub.publish(self.bridge.cv2_to_imgmsg(original_image, "bgr8"))
		pass

if __name__ == "__main__":
	rospy.init_node('finder1')
	f = Finder()

	rospy.spin()
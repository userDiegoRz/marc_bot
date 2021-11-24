#! /usr/bin/env python
import rospy 
import numpy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_msgs.msg import Bool

######
# Multiplexor Node to control All MARC's Auto modes
######

class MainNode():  
	
	def __init__(self):  
		rospy.on_shutdown(self.cleanup)
		#PUBLISHER
		print("Setting publisher")
		self.follower = rospy.Publisher("/control_mode_follower", Bool, queue_size=10)
		self.teleop = rospy.Publisher("/control_mode_teleop", Bool, queue_size=10)
		self.slam = rospy.Publisher("/control_mode_slam", Bool, queue_size=10)
		print("Publisher OK")
		
		print("Starting Variables")
		self.follower_enable = False
		self.teleop_enable = False
		self.slam_enable = False
		
		#SUBSCRIBER
		print("Subscribing to Interface")
		rospy.Subscriber("/control", LaserScan, self.actions) 
		self.rate = rospy.Rate(1)
		
		while not rospy.is_shutdown(): 
			
			self.follower.publish(self.follower_enable)
			self.teleop.publish(self.teleop_enable)
			self.slam.publish(self.slam_enable)
			
			self.rate.sleep() 
		
	def actions(self, control_mode):
		##case grandote 
		if control_mode == "Object follower":
			self.follower_enable = True
			self.teleop_enable = False
			self.slam_enable = False
			break
		if control_mode == "Tele operation":
			self.follower_enable = False
			self.teleop_enable = True
			self.slam_enable = False
			break
		if control_mode == "Slam mapping":
			self.follower_enable = False
			self.teleop_enable = False
			self.slam_enable = True
			break
			
	
		
	def cleanup(self):
		self.follower_enable = False
		self.teleop_enable = False
		self.slam_enable = False
		print("NODE WAS TURNED OFF")

         
if __name__ == "__main__":  
   rospy.init_node('marc_main_node', anonymous=False)  
   try:  
      MainNode()  
   except:  
      rospy.logfatal("Node died")  
      

#! /usr/bin/env python
import rospy 
import numpy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

######
# Multiplexor Node to control All MARC's Auto modes
######

class MainNode():  
	
	def __init__(self):  
		rospy.on_shutdown(self.cleanup)
		#PUBLISHER
		print("Setting publisher")
		self.follower = rospy.Publisher("/control_mode_follower", String, queue_size=10)
		self.teleop = rospy.Publisher("/control_mode_teleop", String, queue_size=10)
		self.nav2d = rospy.Publisher("/control_mode_nav2d", String, queue_size=10)
		print("Publisher OK")
		
		print("Starting Variables")
		self.follower_enable = 'false'
		self.teleop_enable = 'false'
		self.nav2d_enable = 'false'
		
		#SUBSCRIBER
		print("Subscribing to Interface")
		rospy.Subscriber("/interface", String, self.actions) 
		self.rate = rospy.Rate(1)
		
		while not rospy.is_shutdown(): 
			self.follower.publish(self.follower_enable)
			self.teleop.publish(self.teleop_enable)
			self.nav2d.publish(self.nav2d_enable)
			self.rate.sleep() 
		
	def actions(self, control_mode):
		##case grandote
		print(type(control_mode.data)) 
		if control_mode.data == "follower":
			self.follower_enable = 'true'
			self.teleop_enable = 'false'
			self.nav2d_enable = 'false'
			
		elif control_mode.data == "teleop":
			self.follower_enable = 'false'
			self.teleop_enable = 'true'
			self.nav2d_enable = 'false'
			
		elif control_mode.data == "nav2d":
			self.follower_enable = 'false'
			self.teleop_enable = 'false'
			self.nav2d_enable = 'true'
			
		else:
			self.follower_enable = 'false'
			self.teleop_enable = 'false'
			self.nav2d_enable = 'false'
			
		
	def cleanup(self):
		self.follower_enable = 'false'
		self.teleop_enable = 'false'
		self.nav2d_enable = 'false'
		print("NODE WAS TURNED OFF")

         
if __name__ == "__main__":  
   rospy.init_node('marc_main_node', anonymous=False)  
   try:  
      MainNode()  
   except:  
      rospy.logfatal("Node died")  
      

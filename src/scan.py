#! /usr/bin/env python
import rospy 
import numpy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from std_msgs.msg import Bool


class ObjectFollower():  
	
	def __init__(self):  
		rospy.on_shutdown(self.cleanup)
		#PUBLISHER
		print("Setting publisher")
		self.pub = rospy.Publisher("arduino/cmd_vel", Twist, queue_size=10)
		self.measures = rospy.Publisher("debug_values", String, queue_size=10)
		print("Publisher OK")
		
		print("Starting Variables")
		self.vel_msg = Twist()
		self.measure_values = ''
		
		# This variable is to enable the node to publish into arduino/cmd_vel
		self.can_publish = True
		
		self.rad_rpm = 0.10472
		self.max_rpm = 150 # revoluciones por minuto de los motores
		self.max_tics = 11500 # tics de los encoders
		self.safe_dis = 0.6  #distancia maxima a la que se acercara el robot al objeto
		self.k_lin = 0.05 #constante para obtener la velocidad lineal
		self.k_ang = 0.6  #constante para obtener la velocidad angular		
		#SUBSCRIBER
		print("Subscribing to subscriber")
		rospy.Subscriber("/scan", LaserScan, self.ranges_cb) 
		rospy.Subscriber("/control_mode_follower", Bool, self.enable) 
		self.rate = rospy.Rate(1)
		
		while not rospy.is_shutdown(): 
			print("Reading...")
			self.measures.publish(self.measure_values)
			if (self.can_publish):
				self.pub.publish(self.vel_msg) 
			self.rate.sleep() 

	def enable(self, switch):
		self.can_publish = switch.data or True
	
	def ranges_cb(self, msg):
		self.ranges = msg.ranges #arreglo de distancias leidas por el lidar del robot
		self.min_range = min(self.ranges) #distancia minima dentro del arreglo
		self.linear_vel  = self.k_lin*self.min_range #velocidad lineal para x
		self.tics_per_rev = self.max_tics/self.max_rpm
		self.max_lin_vel = self.max_tics*self.rad_rpm # convertir de tics a radianes
		self.angle = msg.angle_min + (msg.angle_increment*self.ranges.index(self.min_range)) #angulo en relacion con el objeto
		self.angular_vel = self.k_ang*self.angle #velocidad angular para z
		
		arefin=[numpy.isfinite(x) for x in self.ranges] #Checks if ranges are "inf" or not
		#self.printFront(self.ranges)
		print("theta = ", self.angle, " \n")
		self.measure_values = str(self.angular_vel)
		if(any(arefin)):#If there is any finite number, there is a detected object
		#detener el movimiento del robot
			
			if self.min_range < self.safe_dis: # cuando encuentra algo dentro de la distancia segura.
				self.vel_msg = Twist()

			elif self.angle > 0.2 or self.angle < -0.2 : # cuando tiene un objeto en la mira
				self.vel_msg = Twist()
				self.vel_msg.angular.z = self.angular_vel
				#self.vel_msg.angular.z = self.angular_vel
			else: # cuando no hay objetos en la mira y nada est[a dentro del rango seguro
				self.vel_msg = Twist()
				self.vel_msg.linear.x = self.linear_vel
				
				
		else:
			self.vel_msg = Twist()
				
				
	def return_in_ranges(self, Min, Max):
		values = [None] * len(msg.ranges)
		for element in msg.ranges:
			if (element > Min and element < Max):
				values.append(element)
		return values
	
	def printFront(self, arr):
		print("right [-2]: ", arr[358])
		print("right [-1]: ", arr[359])
		print("center [0]: ", arr[0])
		print("left [1]: ", arr[1])
		print("left [2]: ", arr[2])
		print("----------------")
	
	def printBack(self, arr):
		print("right [-2]: ", arr[177])
		print("right [-1]: ", arr[178])
		print("center [0]: ", arr[179])
		print("left [1]: ", arr[180])
		print("left [2]: ", arr[181])
		print("----------------")
		
		
	def cleanup(self):
		self.vel_msg = Twist()
		print("NODE WAS TURNED OFF")

         
if __name__ == "__main__":  
   rospy.init_node('scan_values', anonymous=True)  
   try:  
      ObjectFollower()  
   except:  
      rospy.logfatal("Node died")  
      

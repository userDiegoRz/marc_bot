#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String




class VelRemap():
    #This node recieves a Twist message from the cmd_vel_input topic and publishes to cmd_vel a
    # value scaled by some factor to adjust the velocity published by the nav2d operator to work with our simulated robot.
    def __init__(self):
        """ Parameters
        """

        rospy.logdebug("Setting publishers...")
        self.pub_cmd_vel = rospy.Publisher('/arduino/cmd_vel', Twist, queue_size=10)
        self.pub_wtf = rospy.Publisher('/vel_remap_wtf_enters', Twist, queue_size=10)
        
        ############################### SUBSCRIBERS #####################################
        rospy.Subscriber("cmd_vel_input", Twist, self.cmd_vel_cb)
        rospy.Subscriber("control_mode_nav2d", String, self.enable)
        
        ############ CONSTANTS ################
        r=rospy.Rate(10)
        self.cmd_vel_msg = Twist()
        self.can_publish = ''
        
        while not rospy.is_shutdown():
            r.sleep()

    def cmd_vel_cb(self, msg):
        ## This function receives a Twist and copies the linear and angular velocities
        self.pub_wtf.publish(msg)
        
        if (msg.angular.z > 0.11 or  msg.angular.z < -0.11): #asigns absolute 0 to a certain range
            self.cmd_vel_msg = Twist()
            self.cmd_vel_msg.angular.z = msg.angular.z * 1.8
            #limit the maximum angular
            if self.cmd_vel_msg.angular.z > 1.8:
                self.cmd_vel_msg.angular.z = 1.8
            if self.cmd_vel_msg.angular.z < -1.8:
                self.cmd_vel_msg.angular.z = -1.8
        else:
            self.cmd_vel_msg = Twist()
            self.cmd_vel_msg.linear.x = msg.linear.x * 0.06
            #limit the max lineal
            if self.cmd_vel_msg.linear.x > 0.06:
                self.cmd_vel_msg.linear.x = 0.06
        
        if (self.can_publish == 'true'):
            self.pub_cmd_vel.publish(self.cmd_vel_msg)
    
    def enable(self,switch):
        self.can_publish = switch.data
    



    def cleanup(self):
        self.cmd_vel_msg=Twist()
        pass


############################### MAIN PROGRAM ####################################
if __name__ == "__main__":
    rospy.init_node("vel_remap", anonymous=True)
    try:
	    VelRemap()
    except:
        rospy.logfatal("vel_remap died")

#!/usr/bin/env python

import os
import subprocess
import rospy   
from std_msgs.msg import String 
import geometry_msgs.msg
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.core.image import Image
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.lang import Builder

sel = 0
t_count_1 = 0
t_count_2 = 0
next= list()
curentState = str()
timer_count = True
ros_msg = ["Object follower","Tele operation","Slam mapping"]

def cleanup():  
    	pass 

def reset_cb(message_str): 
	pass
		
def pub(text):
	#pass
	pub_dir.publish(text)

def my_callback(dt):
	#currentState=""
	#pub(str(currentState))
	#print(currentState)
	global t_count_1
	t_count_1 = t_count_1 +1
	print(t_count_1)
	if (t_count_1 == 10)and(timer_count):
		t_count_1 = 0
		app.sm.current = "Cara_1"
            
            
def my_callback_2(dt):
	global vel_msg
	global t_count_1
	global t_count_2
	global next
	t_count_1 = 0
	t_count_2 = t_count_2 +1
	if(app.sm.current == "Cara_e_1"):
		app.sm.transition = NoTransition()
		app.sm.current = 'Cara_e_2'
           
	else:
		app.sm.current = 'Cara_e_1'
	if t_count_2 == 5:
		t_count_2 = 0
		app.sm.transition = SlideTransition(direction = 'left')
		#vel_msg.linear.x = 0
		pub(' ')
		#if next[0] == "Enviado":
			#subprocess.Popen(["espeak","-ves-la","paquete entregado, presione terminar para retirarme", "-s100"])
		app.sm.current = next[0]
		next.pop(0)
		return False
            
class MyScreenManager(ScreenManager):
	pass

class Questionary(Screen):
   
	def btn(self, instance):
		title = self.ids.title.text
		global t_count_1
		t_count_1 = 0
		self.manager.current = 'Questionary_2'

class Questionary_2(Screen):
  
	def btn(self, instance):
		global t_count_1
		t_count_1 = 0
		self.manager.current = 'Questionary_end'

class Questionary_end(Screen):
		def btn(self, isntance):
			global t_count_1
			t_count_1 = 0
			self.manager.current = 'Main'

class Envio(Screen):
                
	def btn(self, instance):
		global vel_msg
		#vel_msg.linear.x = 0.1	
		pub(' s')
		print(str(instance.text))
		global timer_count
		timer_count = False
		global t_count_1
		t_count_1 = 0
		global next
		next= ["Enviado","Main"]
		self.manager.current = 'Cara_e_1'
		Clock.schedule_interval(my_callback_2,1)

class Cara_1(Screen):
	def btn(self, instance):
		global t_count_1
		t_count_1 = 0
		self.manager.current = 'Main'

class Cara_e_1(Screen):
	pass

class Cara_e_2(Screen):
	pass

class Enviado(Screen):
	def btn(self, instance):
		global vel_msg
		global timer_count
		timer_count = True
		global t_count_1
		t_count_1 = 0
		self.manager.current = 'Cara_e_1'
		#vel_msg.linear.x = -.1
		#pub()
		Clock.schedule_interval(my_callback_2,1)

class Configuracion(Screen):
	def _init_(self):
		print('que pez')
        
	def btn(self, instance):
		#global currentState
		if(instance.text == "Teleoperado"):
			self.ids['Manual'].background_color = (1,1,1,1)
			self.ids['Follower'].background_color = (1,1,1,1)
			self.ids['Teleop'].background_color = (.1,1,.9,1)
			self.ids['Nav2d'].background_color = (1,1,1,1)
			#currentState = "teleop"
			pub("teleop")
		elif(instance.text ==  "Manual"):
			self.ids['Manual'].background_color = (.1,1,.9,1)
			self.ids['Follower'].background_color = (1,1,1,1)
			self.ids['Teleop'].background_color = (1,1,1,1)
			self.ids['Nav2d'].background_color = (1,1,1,1)
			#currentState = "manual"
			pub("manual")
		elif(instance.text ==  "Navegacion autonoma"):
			self.ids['Manual'].background_color = (1,1,1,1)
			self.ids['Nav2d'].background_color = (.1,1,.9,1)
			self.ids['Teleop'].background_color = (1,1,1,1)
			self.ids['Follower'].background_color = (1,1,1,1)
			#currentState = "nav2d"
			pub("nav2d")
		elif(instance.text ==  "Seguidor"):
			self.ids['Manual'].background_color = (1,1,1,1)
			self.ids['Follower'].background_color = (.1,1,.9,1)
			self.ids['Teleop'].background_color = (1,1,1,1)
			self.ids['Nav2d'].background_color = (1,1,1,1)
			#ScurrentState = "follower"
			pub("follower")
		self.manager.current = 'Main'

class Main(Screen):
   
	def btn(self, instance):      
		if(str(instance.text) == "Ayuda"):
			os.system("echo 'hola profesor arturo  pongale 100 a mis creadores lo merecen ' | festival --tts --language spanish")
			print("ayuda")
		else:
			app.sm.current = str(instance.text)
			global t_count_1
			t_count_1 = 0




class marcApp (App):

	def build(self):
		global event
		self.sm = ScreenManager()
		self.sm.add_widget(Main(name = "Main"))
		self.sm.add_widget(Envio(name = "Envio"))
		self.sm.add_widget(Configuracion(name = "Configuracion"))
		self.sm.add_widget(Questionary(name = "Cuestionario de salud"))        
		self.sm.add_widget(Questionary_2(name = "Questionary_2"))
		self.sm.add_widget(Questionary_end(name = "Questionary_end"))
		self.sm.add_widget(Cara_1(name = "Cara_1"))
		self.sm.add_widget(Cara_e_1(name = "Cara_e_1"))
		self.sm.add_widget(Cara_e_2(name = "Cara_e_2"))
		self.sm.add_widget(Enviado(name = "Enviado"))
		event = Clock.schedule_interval(my_callback,1)
		return self.sm



if __name__ == "__main__":
	
	subprocess.Popen(["rosrun", "rosserial_python", "serial_node.py", "_port:=/dev/ttyACM0"])
	subprocess.Popen(["python3", "/home/gustavo/catkin_ws/src/marc_bot/src/FallenPersonDetector.py"])
	rospy.init_node("UI", anonymous=True) 
	rospy.on_shutdown(cleanup)   
	try:
		pub_dir = rospy.Publisher('/interface', String, queue_size=1) 
		app = marcApp()
	except:
		print("no jalo")
	page = 0
	#pub("manual")
	
	app.run()


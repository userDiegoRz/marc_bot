/*
 *  *  Proyecto de robotica
 *  MARC ROBOT
 *  Version 2.0
 *  21/10/2021
 *  
 *  Programa de control para el MARC ROBOT
 *    STATE 0:
 *      Control de velocidad y direccion con joystick shield de arduino y controlador Roboclaw.
 *    STATE 1:
 *      Navegación autonoma, seguidor de objetos. 
 *    
 *  ------------------------------------------ NOTES-------------------------------------------
 *  NOTES ABOUT ForwardBackward function.
 *  It has has ability to turn the selected motor forwards or backwards. 
 *  The speed value is what determines the direction of rotation. 
 *  The range of values of still 0-127, however now 0 indicates full backwards speed, 
 *  64 in the middle indicates stop, and 127 indicates full forwards speed.
 *  
 *    0   - Full backwards
 *    64  - stop
 *    127 - Full forwards
 *  
 *  NOTES ABOUT ForwardM1 (works the same with BackwardsM1)
 *    0   - Stop
 *    127 - Full forwards
 *  
 *  NOTES ABOUT Direction of the joystick
 *    X   - Left & right        <- 1023 Full left  0 Full right ->
 *    Y   - Forward & Backward  1023 Full forward - 0 Full backward
 *    
 *    -------------------------------- PUBLISHER--------------------------------------
 *    On topic chatter we can debbug the speed values for the left and right wheels.
 *    
 */
 
#include <SoftwareSerial.h>
#include "RoboClaw.h"
#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Float64.h>

//Roboclaw 1 for motor 1 & 2
SoftwareSerial serial(10,11);  
RoboClaw roboclaw(&serial,10000);

//Roboclaw 2 for motor 3 & 4
SoftwareSerial serial2(5,6);  
RoboClaw roboclaw2(&serial2,10000);

//Lectura del puerto A0 y A1 del arduino.
#define PIN_ANALOG_X 0
#define PIN_ANALOG_Y 1

#define address 0x80

//Velocity PID M1 coefficients.
#define Kp 1.83146
#define Ki 0.25606
#define Kd 0
#define qpps 14062

//Velocity PID M2 coefficients.
#define Kp2 1.97657
#define Ki2 0.26720
#define Kd2 0
#define qpps2 13312

//Velocity PID M3 coefficients.
#define Kp3 1.83146
#define Ki3 0.25606
#define Kd3 0
#define qpps3 14062

//Velocity PID M4 coefficients.
#define Kp4 1.97657
#define Ki4 0.26720
#define Kd4 0
#define qpps4 13312

ros::NodeHandle nh;
geometry_msgs::Twist msg;
std_msgs::Float64 speed_l;
std_msgs::Float64 speed_r;

float linear_x;
float angular_z;
const float wheel_dist = 0.5;
const float wheel_rad = 0.06;

const int buttonPin = 8; // the number of the switch pin

ros::Publisher left("left", &speed_l);
ros::Publisher right("right", &speed_r);

void callback(const geometry_msgs::Twist& cmd_vel){
  
  linear_x  = cmd_vel.linear.x;
  angular_z = cmd_vel.angular.z;

  float wheel_right = wR(linear_x,angular_z);
  float wheel_left = wL(linear_x,angular_z);
  
//  speed_l.data = wheel_right;
//  chatter.publish( &speed_l );
 
//  speed_l.data = wheel_left;
//  chatter.publish( &speed_l );

  //speed_l.data = angular_z;
  //chatter.publish( &speed_l );
  
  float wheel_right_map;
  float wheel_left_map;
  float vel_r;
  float vel_l;

  wheel_right_map = mapf(wheel_right,10.0,0.0,0.0,127.0);
  wheel_left_map  = mapf(wheel_left,10.0,0.0,0.0,127.0);

//  wheel_right_map = map(wheel_right,-7.333,17.5,127,0);
//  wheel_left_map  = map(wheel_left,7.666,2.5,127,0);

  vel_r = mapf(angular_z,-1.8,1.8,0.0,127.0);
  vel_l = mapf(angular_z,-1.8,1.8,127.0,0.);

  speed_l.data = vel_l;
  left.publish( &speed_l );
  speed_r.data = vel_r;
  right.publish( &speed_r );

//  if(linear_x == 0.0 && angular_z == 0.0){
//    roboclaw.ForwardBackwardM1(address,64);
//    roboclaw.ForwardBackwardM2(address,64); 
//    roboclaw2.ForwardBackwardM1(address,64);
//    roboclaw2.ForwardBackwardM2(address,64);   
//  }
//  else{
//    roboclaw.ForwardBackwardM1(address,wheel_left_map);
//    roboclaw.ForwardBackwardM2(address,wheel_right_map); 
//    roboclaw2.ForwardBackwardM1(address,wheel_left_map);
//    roboclaw2.ForwardBackwardM2(address,wheel_right_map);
//  } 

  if(linear_x == 0.0 && angular_z == 0.0){
    roboclaw.ForwardBackwardM1(address,64);
    roboclaw.ForwardBackwardM2(address,64); 
    roboclaw2.ForwardBackwardM1(address,64);
    roboclaw2.ForwardBackwardM2(address,64);   
  }
  else if(angular_z == 0){ //avanzar derecho
    roboclaw.ForwardBackwardM1(address,wheel_left_map);
    roboclaw.ForwardBackwardM2(address,wheel_right_map); 
    roboclaw2.ForwardBackwardM1(address,wheel_left_map);
    roboclaw2.ForwardBackwardM2(address,wheel_right_map);
  } 
  else { //giro
    
    if(vel_l < 64){
      vel_l = 10.0;
      vel_r = 120.0;
    }
    else{
      vel_l = 120.0;
      vel_r = 10.0;
    }
    
    roboclaw.ForwardBackwardM1(address,int(vel_l));
    roboclaw.ForwardBackwardM2(address,int(vel_r)); 
    roboclaw2.ForwardBackwardM1(address,int(vel_l));
    roboclaw2.ForwardBackwardM2(address,int(vel_r));
  }      
}


float wR (float linear_v, float angular_v) {
  float wheel_r = 0.0;
  wheel_r = (2*linear_v + angular_v*wheel_dist)/(2*wheel_rad);
  return wheel_r;
}


float wL (float linear_v, float angular_v) {
  float wheel_r = 0.0;
  wheel_r = (2*linear_v - angular_v*wheel_dist)/(2*wheel_rad);
  return wheel_r;
}

float mapf(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

ros::Subscriber<geometry_msgs::Twist> sub("arduino/cmd_vel", callback);

void setup() {
  roboclaw.begin(38400);
  roboclaw2.begin(38400);

  pinMode(buttonPin,INPUT);

  //Set PID Coefficients for the 4 motors
  roboclaw.SetM1VelocityPID(address,Kd,Kp,Ki,qpps);     //M1
  roboclaw.SetM2VelocityPID(address,Kd2,Kp2,Ki2,qpps2); //M2
  roboclaw2.SetM1VelocityPID(address,Kd3,Kp3,Ki3,qpps3);//M3
  roboclaw2.SetM2VelocityPID(address,Kd4,Kp4,Ki4,qpps4);//M4

  //Iniciar robot en velocidad 0
  roboclaw.ForwardBackwardM1(address,64);
  roboclaw.ForwardBackwardM2(address,64); 
  roboclaw2.ForwardBackwardM1(address,64);
  roboclaw2.ForwardBackwardM2(address,64); 

  //Inicializar nodos de ros
  nh.initNode();
  nh.advertise(left);
  nh.advertise(right);
  nh.subscribe(sub);
}


void loop() {
  
  //Automatic Mode Object follower
  nh.spinOnce();
  delay(1);
  if(digitalRead(buttonPin)==HIGH){
    //NOTHING
    nh.spinOnce();
    delay(1);
  }
  //Manual Mode Joystick
  else{
    int dir_x, dir_x_map, speed_y, speed_y_map;
  
    //Lecturas analogicas de los ejes x - z del joystick
    dir_x = analogRead(PIN_ANALOG_X);
    speed_y = analogRead(PIN_ANALOG_Y);
  
    //mapeo de valores del joystick a valores aceptados por roboclaw
    dir_x_map = map(dir_x,0,1023,0,127);   
    speed_y_map = map(speed_y,0,1023,0,127);  
  
    //definir ventana de mapeo en el cual direction = 0
    if(dir_x_map>=61&&dir_x_map<=67)
      dir_x_map = 64;
    //definir ventana de mapeo en el cual speed de motores = 0
    if(speed_y_map>=61&&speed_y_map<=67)
      speed_y_map = 64;

    // Turn clockwise, MARC will turn at a stablish speed of 64.
    if (dir_x_map < 64 && speed_y_map == 64){
      roboclaw.ForwardM2(address,64); 
      roboclaw.BackwardM1(address,64);  
      roboclaw2.ForwardM2(address,64); 
      roboclaw2.BackwardM1(address,64);   
    }
    // Turn anti-clockwise, MARC will turn at a stablish speed of 64.
    else if (dir_x_map > 64 && speed_y_map == 64){
      roboclaw.ForwardM1(address,64);
      roboclaw.BackwardM2(address,64); 
      roboclaw2.ForwardM1(address,64);
      roboclaw2.BackwardM2(address,64); 
    }
    // Turn left 
    else if (dir_x_map > 64){
      roboclaw.ForwardM1(address,speed_y_map);
      roboclaw.BackwardM2(address,0); 
      roboclaw2.ForwardM1(address,speed_y_map);
      roboclaw2.BackwardM2(address,0); 
    }
    // Turn right
    else if (dir_x_map < 64){
      roboclaw.ForwardM2(address,speed_y_map); 
      roboclaw.BackwardM1(address,0);  
      roboclaw2.ForwardM2(address,speed_y_map); 
      roboclaw2.BackwardM1(address,0); 
    }
    // Move straight
    else{
      // Para entender la funcion ForwardBackward, leer la seccion inicial de comentarios del codigo. 
      roboclaw.ForwardBackwardM1(address,speed_y_map);
      roboclaw.ForwardBackwardM2(address,speed_y_map); 
      roboclaw2.ForwardBackwardM1(address,speed_y_map);
      roboclaw2.ForwardBackwardM2(address,speed_y_map); 
    }
  } 
}

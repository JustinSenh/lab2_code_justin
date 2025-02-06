#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point

class rotate_robot_Node(Node):

    def __init__(self):
        super().__init__("rotate_robot_node")
        #Create the subscriber to receive the point coordinate from topic
        self.subscriber_rotate_robot =self.create_subscription(Point, "pixel/location", 
                                        self.rotate_callback, 5)

        #Create the publisher to publish twist message to topic
        self.publisher_rotate_robot =self.create_publisher(Twist, "/cmd_vel", 5)

    #Create callback function for the subscriber. Gets called every time new message published
    def rotate_callback(self, msg:Point):
        self.get_logger().info("Received point")
        x_coordinate = msg.x
        print(x_coordinate)
        # Creates a twist object out of the class and stores it as a variable. Allows us to alter values later
        vel = Twist()
        vel.angular.z= 0.0


        #write an if statement to compare x coordinate to screen center
        if x_coordinate < 110:
            #rotate robot counterclockwise 1
            vel.angular.z = 1.0
            self.publisher_rotate_robot.publish(vel)
        elif x_coordinate > 210:
            #rotate robot clockwise -1
            vel.angular.z = -1.0
            self.publisher_rotate_robot.publish(vel)
        else:
            #don't rotate the robot
            vel.angular.z = 0.0
            self.publisher_rotate_robot.publish(vel)
        print(x_coordinate)
        self.publisher_rotate_robot.publish(vel)



def main(args=None):
    rclpy.init(args=args)
    node = rotate_robot_Node()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()




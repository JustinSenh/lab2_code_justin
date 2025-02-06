#!usr/bin/env pyhon3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
import cv2
import numpy as np
import cv_bridge
from geometry_msgs.msg import Point  # Added import for Point message
from cv_bridge import CvBridge

class find_object_Node(Node):
    def __init__(self):
        super().__init__("find_object_node")
        #create the subscriber part of this node. 
        self.subscriber_find_object = self.create_subscription(CompressedImage,
                         "image_raw/compressed", self.image_callback, 5)
        #create the publisher part of this node. 
        self.publisher_find_object = self.create_publisher(Point, "pixel/location",5)

        self.bridge = CvBridge()
    #create the callback function for the subscriber. tells us how often it subscribes. 
    # this gets called whenever a new message gets published
    def image_callback(self, msg:CompressedImage):
        self.get_logger().info("Received compressed image")
        np_arr = np.frombuffer(msg.data, np.uint8) #converts compressed image to numpy array
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) #converts that array into HSV image so we can proceed

        ##Now we start to integrate the lab 1 code

        #immediately define the color ranges
        lower_red1 = np.array([0,120,70])
        upper_red1 = np.array([10,255,255])
        lower_red2 = np.array([170,120,70])
        upper_red2 = np.array([180,255,255])
        blurred = cv2.GaussianBlur(frame, (11,11), 0)
        hsvframe= cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        #Create mask for red color
        mask1 = cv2.inRange(hsvframe, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsvframe, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1,mask2)

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, None)

        contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        published = False
        if contours:
            # Filter out small contours based on area
            min_area = 100
            contours = [c for c in contours if cv2.contourArea(c) > min_area]

            if contours:
                #find largest contour
                max_contour = max(contours, key=cv2.contourArea)

                #get bounding box for the largest contour
                x,y,w,h = cv2.boundingRect(max_contour)

                #draw bounding box around tracked object
                cv2.rectangle(frame, (x,y), (x+2,y+h), (0,255,0),2)

                #find centroid
                cx = int(x+w/2)
                cy = int(y+h/2)
                cv2.circle(frame, (cx,cy), 5,(0,0,225), -1)
                print(cx,cy)
                point = Point(x=float(cx), y=float(cy), z=0.0)  # Create a Point message
                self.publisher_find_object.publish(point)  # Publish the Point
                published = True
                h,w = mask.shape
                #print("Height:", h)
                #print("Width", w)

        if published == False:
            point = Point(x=160.0, y=0.0, z=0.0)
            self.publisher_find_object.publish(point)
            

def main(args=None):
    rclpy.init(args=args)
    node = find_object_Node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

#!/usr/bin/python2

import os
import sys
import argparse

import rospy

import cv2
import cv_bridge
import rospkg

from sensor_msgs.msg import (
    Image,
)


def send_image(path):
    """
    Send the image located at the specified path to the head
    display on Baxter.

    @param path: path to the image file to load and send
    """
    img = cv2.imread(path)
    msg = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
    pub = rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=1)
    pub.publish(msg)
    # Sleep to allow for image to be published.
    rospy.sleep(1)


def main():
    rospy.init_node('rsdk_xdisplay_image', anonymous=True)
    rospack = rospkg.RosPack()
    path = rospack.get_path('baxter_alvar')
    filename = os.path.join(path, "images/marker1.png")

    if not os.access(filename, os.R_OK):
        rospy.logerr("Cannot read file")
        return 1

    send_image(filename)
    return 0

if __name__ == '__main__':
    sys.exit(main())

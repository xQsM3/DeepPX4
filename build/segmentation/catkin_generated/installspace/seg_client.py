#!/usr/bin/env python3
from __future__ import print_function

import sys
import rospy
from segmentation.srv import *
from segmentation.msg import SegImage
from mavros_msgs.msg import CameraImageCaptured

import cv2 as cv
from cv_bridge import CvBridge

def segmentation_client(image_topic):
    # get image from drone camera

    #im = cv.imread("/home/xqsme/Pictures/test.png")
    #im = CvBridge().cv2_to_imgmsg(im,encoding="passthrough")
    im = rospy.wait_for_message(image_topic, CameraImageCaptured,timeout=20)
    seg_msg = SegImage()
    seg_msg.image = im
    seg_msg.header.stamp = rospy.Time.now()
    rospy.wait_for_service("segmentation")

    try:
        seg = rospy.ServiceProxy("segmentation",Segmentation)
        print(seg.request_class._type )
        print(seg_msg._type)
        #im._type = "segmentation/SegmentationRequest"

        pred_msg = seg(seg_msg) # get segmentation from seg model service

        pred = CvBridge().imgmsg_to_cv2(pred_msg.segimage.image,desired_encoding="passthrough")
        cv.namedWindow("prediction",cv.WINDOW_NORMAL)
        cv.imshow("prediction",pred)
        cv.waitKey()
        return pred_msg
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return f"args should be [image_topic]"

if __name__ == "__main__":
    if len(sys.argv) == 2:
        image_topic = sys.argv[1]
    else:
        raise ValueError(usage())
    rospy.init_node("segmentation_client")
    segmentation_client(image_topic)





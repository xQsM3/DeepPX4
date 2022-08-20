#!/usr/bin/env python
from __future__ import print_function

import sys
import rospy,roslaunch,rospkg
from utils import seg_client,fix_melodic
from sensor_msgs.msg import Image

import cv2 as cv
import argparse
from cv_bridge import CvBridge


class Px4Tuner():
    '''
    class which handles the parameter tuning of px4
    looks up best parameters for current segmentation state,
    and requests ros service to adjust parameters
    '''
    def __init__(self,lut_path):
        self.LUT = self.load_table(lut_path)
    def load_table(self,lut_path):
        pass


def tuning_loop(image_topic, hz, lut_path):
    pub = segmentation_publisher()
    tune = Px4Tuner(lut_path=lut_path)
    rate = rospy.Rate(hz)
    while not rospy.is_shutdown():
        # get segmentation and publish it
        pred = seg_client.segmentation_client(image_topic)
        print(pred.shape)
        if fix_melodic.CvBridgeMelodic().fix_needed():
            im_msg = fix_melodic.CvBridgeMelodic().cv2_to_imgmsg(pred,encoding="bgr8")
        else:
            im_msg = CvBridge().cv2_to_imgmsg(pred,encoding="passthrough")
        pub.publish(im_msg)





        rate.sleep()

def segmentation_publisher():
    pub = rospy.Publisher("segmentation_image",Image,queue_size=10)
    return pub


def usage():
    return f"args should be [image_topic,hz]"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '--image_topic',
        help='image topic of ros',
        default='/camera_front/rgb/image_raw',
        type=str)
    parser.add_argument(
        '--hz',
        help='refreshing rate',
        default='2',
        type=int)
    parser.add_argument(
        '--lut_path',
        help='look up table path',
        default='lut.csv',
        type=str)
    pargs = parser.parse_args()

    package = 'segmentation'
    executable = 'seg_service.py'
    node_name = 'segmentation_server'
    node = roslaunch.core.Node(package=package, node_type=executable, name=node_name,args="configs/ppliteseg_hannasscapes.yml cpu")
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()
    process = launch.launch(node)

    seg_client.init()
    tuning_loop(pargs.image_topic, pargs.hz, pargs.lut_path)





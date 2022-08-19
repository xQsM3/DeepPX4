#!/usr/bin/env python3

from __future__ import print_function
from segmentation.srv import Segmentation
import rospy

import argparse
from nn.model import NN
from libs import inf_config
import cv2 as cv
from cv_bridge import CvBridge
from segmentation.msg import SegImage

def handle_segmentation(msg):
    global model
    im = CvBridge().imgmsg_to_cv2(msg.segimage.image,desired_encoding="passthrough")
    pred = model(im)

    seg_msg = SegImage()
    seg_msg.header.stamp = rospy.Time.now()
    seg_msg.image = CvBridge().cv2_to_imgmsg(pred,encoding="passthrough")
    return seg_msg

def segmentation_server():
    rospy.init_node("segmentation_server")
    seg_serv = rospy.Service("segmentation",Segmentation,handle_segmentation)
    print("segmentation service is ready")
    rospy.spin()

def model_init(pargs):
    # get model config args
    config_args = inf_config.ConfigArgs(pargs.config)
    # get user args
    config_args.device = pargs.device
    # load model with config
    model = NN(config_args)
    print("segmentation model initialized")
    return model


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SegmentationService')
    parser.add_argument(
        '--config',
        help='inference config of model, full or relative path',
        default='configs/ppliteseg_hannasscapes.yml',
        type=str)
    parser.add_argument(
        '--device',
        help='device, e.g. cpu or gpu',
        default='cpu',
        type=str)
    pargs = parser.parse_args()

    model = model_init(pargs)
    segmentation_server()

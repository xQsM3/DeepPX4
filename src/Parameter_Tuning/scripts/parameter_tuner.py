#!/usr/bin/env python
from __future__ import print_function

import sys
import rospy,roslaunch,rospkg
from utils import seg_client,fix_melodic
from sensor_msgs.msg import Image

import pandas as pd
import numpy as np
import dynamic_reconfigure.client

import argparse
from cv_bridge import CvBridge

from utils import visualize
from libs import inf_config


class ImageListener():
    def __init__(self,image_topic):
        rospy.Subscriber(image_topic,Image,self.callback)
        self.im_msg = rospy.wait_for_message(image_topic,Image,timeout=20)
    def callback(self,im_msg):
        self.im_msg = im_msg
class Px4Tuner():
    '''
    class which handles the parameter tuning of px4
    looks up best parameters for current segmentation state,
    and requests ros service to adjust parameters
    '''
    def __init__(self,lut_path,model_config):
        rospy.init_node("px4_parameter_tuner")
        self._LUT = self._load_table(lut_path)
        self._cls_num, self._clss = self._get_clss(model_config)
        self.change_params = dynamic_reconfigure.client.Client("local_planner_nodelet")

    def request_parameter_change(self,im):
        i = self._analyze_state(im)
        params = self._lookup(i)
        try:
            config = self.change_params.update_configuration(params)
            print("ParamSet successfull")
        except rospy.ServiceException as e:
            print("failed ParamSet")

    def _analyze_state(self,im):
        # analyze segmentation state and suggest px4 parameters
        if self._class_share(im,0.5)[3] > 0.8: # if 80% of "horizon" strip (upper 50% of image) is from class sky
            i = 0 # use simple world params
        elif self._class_share(im,0.1)[3] > 0.9: # if 90% of 10% upper strip if sky
            i = 1 # use small city params
        elif self._class_share(im,0.5)[3] < 0.1: # if almost all horozion view is blocked, assume big city
            i = 3
        else: # else assume middle sized city
            i = 2
        return i

    def _get_clss(self, model_config_path):
        model_config = inf_config.ConfigArgs(model_config_path)
        cls_num = len(model_config.custom_color) //3
        return cls_num,[i for i in range(0,cls_num)]

    def _class_share(self,im,p):
        strip = self._strip(im,p)
        n = strip.size
        distribution = [np.count_nonzero(strip==c) / n for c in self._clss]
        return distribution

    def _load_table(self, lut_path):
        df = pd.read_csv(lut_path)
        return df

    def _lookup(self,i):
        # looks up best parameters from LUT and stores them in a dictionaryformat for dynamic reconfigure service
        params = dict(zip(self._LUT.loc[i].index,self._LUT.loc[i]))
        return params

    def _strip(self,im,p):
        # crops upper strip of image in percent (p)
        height = im.shape[0]
        height_strip = round(height * p )
        strip = im[0:height_strip,:]
        return strip

def get_color_map(model_config_path):
    model_config = inf_config.ConfigArgs(model_config_path)
    return visualize.get_color_map_list(256, custom_color=model_config.custom_color)

def tuning_loop(image_topic, hz, lut_path,model_config_path):
    pub = segmentation_publisher()
    tune = Px4Tuner(lut_path=lut_path,model_config=model_config_path)
    rate = rospy.Rate(hz)
    color_map = get_color_map(model_config_path)
    im_listener = ImageListener(image_topic)

    while not rospy.is_shutdown():
        # get segmentation
        pred = seg_client.segmentation_client(image_topic,im_listener.im_msg)
        # publish colored segmentation
        pred_colored = visualize.addcolor(pred,color_map)
        if fix_melodic.CvBridgeMelodic().fix_needed():
            im_msg = fix_melodic.CvBridgeMelodic().cv2_to_imgmsg(pred_colored,encoding="bgr8")
        else:
            im_msg = CvBridge().cv2_to_imgmsg(pred_colored,encoding="passthrough")
        pub.publish(im_msg)
        #calculate new px4 parameters and publish
        tune.request_parameter_change(pred)

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
    parser.add_argument(
        '--config',
        help='seg model config',
        default='configs/ppliteseg_hannasscapes.yml',
        type=str)
    parser.add_argument(
        '--device',
        help='device for NN model either cpu or gpu',
        default='cpu',
        type=str)
    pargs = parser.parse_args()

    package = 'segmentation'
    executable = 'seg_service.py'
    node_name = 'segmentation_server'
    node = roslaunch.core.Node(package=package, node_type=executable, name=node_name,args=f"{pargs.config} {pargs.device}")
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()
    process = launch.launch(node)


    tuning_loop(pargs.image_topic, pargs.hz, pargs.lut_path, pargs.config)





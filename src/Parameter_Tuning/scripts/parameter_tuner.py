#!/usr/bin/env python
from __future__ import print_function

import math
import sys
import json
import rospy,roslaunch,rospkg
from utils import seg_client,fix_melodic
from sensor_msgs.msg import Image

import pandas as pd
import numpy as np
import dynamic_reconfigure.client

import argparse
from cv_bridge import CvBridge

from utils import visualize,cv_utils,math_utils,kin_utils,geometry_utils
from libs import inf_config
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TwistStamped
from visualization_msgs.msg import MarkerArray
from utils.ros_com import im_array2im_msg,publish_xypath,DroneStateListener,GoalListener,ImageListener

class Px4Tuner():
    '''
    handles the parameter tuning of px4
    looks up best parameters for current segmentation state,
    and requests ros service to adjust parameters
    '''
    def __init__(self,lut_path,model_config,labels):
        rospy.init_node("px4_parameter_tuner")
        self._LUT = self._load_table(lut_path)
        self._cls_num, self._clss = self._get_clss(model_config)
        self.change_params = dynamic_reconfigure.client.Client("local_planner_nodelet")
        self._labels = self._load_labels(labels)

        self.drone = DroneStateListener(pose_topic="/mavros/global_position/local", pose_type=Odometry,
                                        vel_topic="/mavros/local_position/velocity_local",vel_type=TwistStamped)
        self.goal = GoalListener(goal_topic="/goal_position", type=MarkerArray)

        self.path = math_utils.Polyline([(self.drone.pos.x,self.drone.pos.y,
                                          self.drone.pos.z,rospy.get_time())]) # drone path
        self._fixing_stucked = 0
    def request_parameter_change(self,im):
        params = self._analyze_state(im)
        try:
            config = self.change_params.update_configuration(params)
            print("ParamSet successfull")
        except rospy.ServiceException as e:
            print("failed ParamSet")
    def _ascending(self):
        return True if abs(self.drone.vel_linear.z) >= 0.06 else False
    def _analyze_state(self,im):
        self._update_path()
        print("PARAMETER TUNING")
        print(f"above 50% skyvision in %: {self._class_share(im,0.5)[self._labelID('sky')]}")
        print(f"above 10% skyvision in %: {self._class_share(im,0.1)[self._labelID('sky')]}")
        # analyze segmentation state and suggest px4 parameters
        
        if self._class_share(im,0.5)[self._labelID("sky")] > 0.8: # if x% of "horizon" strip (upper 50% of image) is from class sky
            params = self._lookup(0) # use simple world params
        elif self._class_share(im,0.1)[self._labelID("sky")] > 0.9: # if x0% of y% upper strip if sky
            params = self._lookup(1) # use small city params
        elif self._class_share(im,0.5)[self._labelID("sky")] < 0.1: # if almost all horozion view is blocked, assume big city
            params = self._lookup(3)
        else: # else assume middle sized city
            params = self._lookup(2)

        # special cases
        if self._stucked():
            print("DRONE IS STUCKED, DESTUCK MODE")
            params = self._lookup(0) # go in emergency param set if stucked

        print(f"transfer params {params}")
        return params

    def _compute_goal_distance(self):
        goal_pose = self.goal.pos.pos_asarray
        drone_pose = self.drone.pos.pos_asarray
        return np.linalg.norm(goal_pose-drone_pose)

    def _compute_goal_angle_arroundaxis(self,axis="z"):
        assert (axis=="x" or axis=="y" or axis=="z" ), "axis musst be x,y or z as string"
        goal_pose = self.goal.pos.pos_asarray
        drone_pose = self.drone.pos.pos_asarray
        goal_vector = goal_pose-drone_pose
        if axis=="x":
            axis_vector = np.array([1, 0, 0])
        elif axis=="y":
            axis_vector = np.array([0,1,0])
        else:
            axis_vector = np.array([0,0,1])
        a = geometry_utils.angle_between(goal_vector,axis_vector)
        return a
    def _get_clss(self, model_config_path):
        model_config = inf_config.ConfigArgs(model_config_path)
        cls_num = len(model_config.custom_color) //3
        return cls_num,[i for i in range(0,cls_num)]

    def _class_share(self,im,p):
        strip = self._strip(im,p)
        n = strip.size
        distribution = [np.count_nonzero(strip==c) / n for c in self._clss]
        return distribution
    def _head_toe_goal(self,angle_thresh):
        a_border1 = angle_thresh * math.pi / 180
        a_border2 = math.pi - a_border1
        angle = self._compute_goal_angle_arroundaxis(axis="z")
        if angle < a_border1 or angle > a_border2:
            return True
        return False

    def _labelID(self,cls_name):
        # returns train id of specific class
        return self._labels[cls_name]["trainID"]
    def _load_labels(self,label_path):
        label_path = inf_config.relative_to_abs_path(label_path)
        with open(label_path) as json_file:
            labels = json.load(json_file)
        return labels
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

    def _stucked(self,approach_limit=10,intersec_limit=2,fixfor=5):
        intersections = self.path.SelfIntersections() # determine intersections
        # post process intersections, pop out intersections which do not match criteria
        intersections = math_utils.postprocess_intersections(intersections, timethresh=10, z_thresh=1)
        approaches = self.path.SelfApproaches(distancethresh=1,timethresh=10)

        publish_xypath(self.path, intersections,
                       approaches, self._fixing_stucked)  # draw path and intersections, publish

        if len(intersections) > intersec_limit: # if path self intersections reached
            self._fixing_stucked += 1
            if self._fixing_stucked >= fixfor:
                self._fixing_stucked = 0
                self.path = math_utils.Polyline([(self.drone.pos.x, self.drone.pos.y)])  # reset drone path recording
            return True
        return False
    def _update_path(self):
        self.path.Add(self.drone.pos.x,self.drone.pos.y,
                      self.drone.pos.z,rospy.get_time())

def tuning_loop(image_topic, hz, lut_path,model_config_path):
    seg_pub = rospy.Publisher("segmentation_image",Image,queue_size=10)
    tune = Px4Tuner(lut_path=lut_path,model_config=model_config_path,labels=pargs.labels)
    rate = rospy.Rate(hz)
    color_map = visualize.get_color_map(model_config_path)
    im_listener = ImageListener(image_topic)
    while not rospy.is_shutdown():
        # get segmentation
        pred = seg_client.segmentation_client(image_topic,im_listener.im_msg)
        # publish colored segmentation
        pred_colored = visualize.addcolor(pred,color_map)
        im_msg = im_array2im_msg(pred_colored)
        seg_pub.publish(im_msg)
        #calculate new px4 parameters and publish
        tune.request_parameter_change(pred)

        rate.sleep()

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
        default='10',
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
        '--labels',
        help='seg model label path',
        default='weights/ppliteseg_hannasscapes/labels.json',
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

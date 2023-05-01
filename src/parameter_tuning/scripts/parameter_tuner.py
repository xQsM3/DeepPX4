#!/usr/bin/env python
from __future__ import print_function

import math
import sys,os
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
from std_msgs.msg import String
from visualization_msgs.msg import MarkerArray
from utils.ros_com import im_array2im_msg,publish_xypath,DroneStateListener,GoalListener,ImageListener
from utils.camera_utils import Camera
class Px4Tuner():
    '''
    handles the parameter tuning of px4
    looks up best parameters for current segmentation state,
    and requests ros service to adjust parameters
    '''
    def __init__(self,model_config,labels,dynreconfigure_name,goal,color_map):
        rospy.init_node("px4_parameter_tuner")
        self._LUT = self._load_table()
        self.color_map = color_map
        self._cls_num, self._clss = self._get_clss(model_config)
        self.change_params = dynamic_reconfigure.client.Client(dynreconfigure_name)
        self._labels = self._load_labels(labels)

        self.drone = DroneStateListener(pose_topic="/mavros/global_position/local", pose_type=Odometry,
                                        vel_topic="/mavros/local_position/velocity_local",vel_type=TwistStamped)
        self.goalpos = goal
        self.init_goal_z(goal)
        self.camera = Camera(info_topic="/camera_front/rgb/camera_info",
                             image_topic="/segmentation_image")
        self.debug_pub = rospy.Publisher("/debug",String,queue_size=10)
        self.path = math_utils.Polyline([(self.drone.pos.x,self.drone.pos.y,
                                          self.drone.pos.z,rospy.get_time())]) # drone path

    def init_goal_z(self,goal):
        #gives initial goal z parameter to dyn reconfigure
        params = {"goal_z_param":goal.z}
        self.change_params.update_configuration(params)
    def request_parameter_change(self,im):
        params = self._analyze_state(im)
        try:
            config = self.change_params.update_configuration(params)
            print(f"ParamSet successfull: {config}")
        except rospy.ServiceException as e:
            print("failed ParamSet")
    def _ascending(self):
        return True if abs(self.drone.vel_linear.z) >= 0.06 else False
    def _analyze_state(self,im):
        print("PARAMETER TUNING")

        roi,goal_proj = self.determine_roi(widthp=0.3,heightp=0.3)
        print(f"above 20% skyvision in %: {self._class_share(self._crop(im,roi))[self._labelID('sky')]}")
        if roi:
            self.camera.publish_roi_segmentation(roi,goal_proj,visualize.addcolor(im,self.color_map))

        # analyze segmentation state and suggest px4 parameters
        if self._class_share(self._crop(im,roi))[self._labelID("sky")] < 0.6:
            # parameter study inspired params
            params = self._lookup(3)
            # bio inspired params
            params["goal_z_param"] = self.tune_goalz(climb_angle=20)  # max in config is 5000
        else:
            params = self._lookup(0)
            params["goal_z_param"] = self.drone.pos.z #hold altitude

        # reset goal z near to goal, or if sky is free
        roi_descending = roi
        roi_descending.h = roi.h * 2
        if self._compute_goal_distance(xy=True) < 15 or \
                self._class_share(self._crop(im,roi_descending))[self._labelID("sky")] > 0.8 or \
                not self.goal_projection_is_obstacle(goal_proj=goal_proj,image=im):
            params["goal_z_param"] = self.goalpos.z

        self.debug_pub.publish(f"xy_goal_distance: {self._compute_goal_distance()}"
                               f"projected goal {goal_proj.x,goal_proj.y}"
                               f"goal sky/road class: {not self.goal_projection_is_obstacle(goal_proj=goal_proj,image=im)}")


        if self._class_share(self._crop(im,roi_descending))[self._labelID("tree")] > 0.1:
            params["obstacle_cost_param_"] = 15
        return params

    def goal_projection_is_obstacle(self,goal_proj,image):
        # returns false if goal projection point belongs to sky
        # note this is primitive, does not check if goal is in front of a building..
        if not goal_proj.x or not goal_proj.y:
            return True
        if image[int(goal_proj.y), int(goal_proj.x)][0] == self._labelID("sky"):
            return False
        if image[int(goal_proj.y), int(goal_proj.x)][0] == self._labelID("road"):
            return False
        return True

    def determine_roi(self,widthp=0.3,heightp=0.2):
        # project goal on image
        goalpos = np.array([self.goalpos.x,self.goalpos.y,self.goalpos.z]).reshape(3,1)
        goal_projection = self.camera.project_worldpoint_2_cameraplane(goalpos)

        # take whole image width as roi if goal is not visible / projectable
        if not goal_projection.x or not goal_projection.y:
            roi = math_utils.Box(x=0,
                                 y=0,
                                 w=self.camera.width,
                                 h=int(self.camera.height*heightp))
            return roi,goal_projection

        # otherwise, create roi around goal x coordinate
        roi = math_utils.Box(x = int(goal_projection.x - self.camera.width * widthp / 2),
                             y = 0, #y = int(goal_projection.y - self.camera.height * heightp / 2),
                             w = int(self.camera.width * widthp),
                             h = int(self.camera.width * heightp))
        return roi,goal_projection

    def tune_goalz(self,climb_angle):
        distance = self._compute_goal_distance(xy=True)
        return self.drone.pos.z + distance * math.tan(climb_angle / 180 * math.pi)
    def _compute_goal_distance(self,xy=False):
        goal_pose = self.goalpos.pos_asarray
        drone_pose = self.drone.pos.pos_asarray
        if xy: #compute distance in xy plane
            goal_pose[2],drone_pose[2] = 0,0
        return np.linalg.norm(goal_pose-drone_pose)

    def _get_clss(self, model_config_path):
        model_config = inf_config.ConfigArgs(model_config_path)
        cls_num = len(model_config.custom_color) //3
        return cls_num,[i for i in range(0,cls_num)]

    def _class_share(self,im):
        n = im.size
        distribution = [np.count_nonzero(im==c) / n for c in self._clss]
        return distribution

    def _labelID(self,cls_name):
        # returns train id of specific class
        return self._labels[cls_name]["trainID"]
    def _load_labels(self,label_path):
        label_path = inf_config.relative_to_abs_path(label_path)
        with open(label_path) as json_file:
            labels = json.load(json_file)
        return labels
    def _load_table(self):
        lut_path = os.path.join(rospkg.RosPack().get_path("parameter_tuning"),"scripts/lut.csv")
        df = pd.read_csv(lut_path)
        return df

    def _lookup(self,i):
        # looks up best parameters from LUT and stores them in a dictionaryformat for dynamic reconfigure service
        params = dict(zip(self._LUT.loc[i].index,self._LUT.loc[i]))
        return params

    def _crop(self,im,roi):
        crop = im[roi.y:roi.y+roi.h,roi.x:roi.x+roi.w]
        return crop

    def _strip(self,im,p):
        # crops upper strip of image in percent (p)
        height = im.shape[0]
        height_strip = round(height * p )
        strip = im[0:height_strip,:]
        return strip

    def _update_path(self):
        self.path.Add(self.drone.pos.x,self.drone.pos.y,
                      self.drone.pos.z,rospy.get_time())
    def _hover(self):
        # returns true if drones velocity in x / y is almost 0
        if abs(self.drone.vel_linear.x) <= 0.05 or \
                abs(self.drone.vel_linear.y <= 0.05):
            return True
        else:
            return False
def tuning_loop(image_topic, hz,model_config_path,scale,dynreconfigure_name,goal_z):
    seg_pub = rospy.Publisher("segmentation_image",Image,queue_size=10)
    color_map = visualize.get_color_map(model_config_path)
    tune = Px4Tuner(model_config=model_config_path,labels=pargs.labels,
                    dynreconfigure_name=dynreconfigure_name,goal=goal,
                    color_map=color_map)
    rate = rospy.Rate(hz)
    color_map = visualize.get_color_map(model_config_path)
    im_listener = ImageListener(image_topic)
    while not rospy.is_shutdown():
        # get segmentation
        pred = seg_client.segmentation_client(image_topic,im_listener.im_msg,scale=scale)
        # publish colored segmentation
        pred_colored = visualize.addcolor(pred,color_map)
        im_msg = im_array2im_msg(pred_colored)
        seg_pub.publish(im_msg)
        #calculate new px4 parameters and publish
        tune.request_parameter_change(pred)

        rate.sleep()

def read_rosparams(args):
    try:
        args.dynreconfigure_name = rospy.get_param("px4_parameter_tuner/dynreconfigure_name")
    except:
        pass
    return args
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
        '--scale',
        help='scale of segmentation model input image, 1 and 0.5 tested ',
        default='1.',
        type=float)
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
    parser.add_argument(
        '--dynreconfigure_name',
        help='name of dynamic reconfigure nodelet topic',
        default="local_planner_nodelet",
        type=str)
    parser.add_argument(
        '--goal',
        type=str,
        required=True)




    try:
        pargs = parser.parse_args()
    except:
        pargs, unknown = parser.parse_known_args()
    pargs = read_rosparams(pargs) # read parameters from launch file, if tuner was started by roslaunch

    # start segmentaiton node @todo: change this to launch file
    package = 'segmentation'
    executable = 'seg_service.py'
    node_name = 'segmentation_server'
    node = roslaunch.core.Node(package=package, node_type=executable, name=node_name,args=f"{pargs.config} {pargs.device}")
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()
    process = launch.launch(node)

    goal_list = pargs.goal.split(" ")
    goal = kin_utils.Pose(x=float(goal_list[0]),
                               y=float(goal_list[1]),
                               z=float(goal_list[2]))
    tuning_loop(pargs.image_topic, pargs.hz, pargs.config,pargs.scale,pargs.dynreconfigure_name,goal)

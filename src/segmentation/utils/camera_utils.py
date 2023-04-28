#!/usr/bin/env python

from sensor_msgs.msg import CameraInfo,Image
from gazebo_msgs.srv import GetModelState
from rosgraph_msgs.msg import Clock
from utils.ros_com import ImageListener,im_array2im_msg
import rospy
import numpy as np
import utils.math_utils as math_utils
import cv2 as cv
import pyquaternion
import math

class Camera:
    def __init__(self, info_topic,image_topic):
        #rospy.init_node("camera_node", anonymous=True)
        resp = rospy.wait_for_message(info_topic, CameraInfo, timeout=5)
        self.K = np.asarray(resp.K).reshape(3,3) #intrinsic camera matrix
        self.D = resp.D #distortion
        self.P = np.asarray(resp.P).reshape(3,4) # projection/camera matrix
        self.height = resp.height
        self.width = resp.width


        self.im_pub = rospy.Publisher("segmentation_image/roi", Image, queue_size=10)
        self.get_camstate = rospy.ServiceProxy("/gazebo/get_model_state",GetModelState)
    def project_worldpoint_2_cameraplane(self, world_point_WCOS):
        #  http://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/CameraInfo.html
        # https://wiki.ros.org/image_pipeline/CameraInfo

        # project point
        X_dash = self.world_2_camera_transformation(world_point_WCOS)
        x_norm_undistored = X_dash / X_dash[2]
        q = np.squeeze(self.K.dot(x_norm_undistored) )
        x,y = q[0],q[1]

        if np.isinf(x) or np.isinf(y) or \
                np.isnan(x) or np.isnan(y) or \
                x < 0 or y < 0 or \
                x > self.width or y > self.height:
            return math_utils.Point2D(x=None,y=None)
        return math_utils.Point2D(x=q[0],y=q[1])

    def world_2_camera_transformation(self,point_WCOS):
        #https://www.cse.psu.edu/~rtc12/CSE486/lecture12.pdf
        state_resp = self.get_camstate(model_name="iris_obs_avoid")
        cam_position = np.array([state_resp.pose.position.x,
                                 state_resp.pose.position.y,
                                 state_resp.pose.position.z]).reshape(3,1)

        cam_quaternion = pyquaternion.Quaternion(w=state_resp.pose.orientation.w,
                                                 x=state_resp.pose.orientation.x,
                                                 y=state_resp.pose.orientation.y,
                                                 z=state_resp.pose.orientation.z)
        # rotate cam quaternion from ROS definition (x -> view direction) to common definition (z -> view direction)
        q_x_90 = pyquaternion.Quaternion(axis=[1, 0, 0], angle=-math.pi / 2)
        q_y_90 = pyquaternion.Quaternion(axis=[0, 1, 0], angle=-math.pi / 2)
        q_z_180 = pyquaternion.Quaternion(axis=[0, 0, 1], angle=math.pi)
        q_camcos_transfer = q_z_180 * q_y_90 * q_x_90
        cam_quaternion = q_camcos_transfer * cam_quaternion.inverse

        # translate point
        point = point_WCOS - cam_position
        # rotate point
        return np.array([cam_quaternion.rotate(point)]).reshape(3,1)

    def publish_roi_segmentation(self,roi,goalprojection,im):
        image = cv.resize(im,(self.width,self.height))
        image = cv.rectangle(image,(roi.x,roi.y),
                             (roi.x+roi.w,roi.y+roi.h),
                             (0,0,0),15)
        if goalprojection.x and goalprojection.y:
            image = cv.circle(image, (int(goalprojection.x), int(goalprojection.y)),
                              int(self.width // 80), (0, 0, 0), -1)
        im_msg = im_array2im_msg(image)
        self.im_pub.publish(im_msg)



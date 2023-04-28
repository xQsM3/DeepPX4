#include <ros/ros.h>
#include <vector>
#include <string>
#include <boost/foreach.hpp>
#include <stdio.h>

#include "local_planner/local_planner.h"

#include <pcl_ros/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/common/common.h>

#include <sensor_msgs/PointCloud.h>
#include <sensor_msgs/PointCloud2.h>
#include <sensor_msgs/point_cloud_conversion.h>

#include <algorithm>
#include <iterator>

double close_obst;

void cloud_callback (const sensor_msgs::PointCloud2ConstPtr& cloud_msg){
	sensor_msgs::PointCloud out_cloud;
	FILE* FilePtr;
	int fail;

	double PI = 3.14159265358979323846;

	double speed_prop = 2.5; //proportionality factor to determine the flight speed
	std::vector <double> lat_dist; //lateral distance between obstacle and flight path
	double gamma; //angle [deg] between point and flight direction in XY-plane
	double beta; //angle [deg] between point and flight direction in the XZ-plane
	double alpha_XY; //angle of point in XY-Plane
	double alpha_XZ; //angle of point in XZ-Plane
	double geo_angl_XY = 20./180*M_PI; //angle [deg] between image plane and flight direction in XY-plane
	double geo_angl_XZ = 0; //angle between image plane and flight direction in XZ-plane
	double geo_dist_Y = 0.2; //distance [m] between Sensor and CG of Drone in Y-Direction
	

	sensor_msgs::convertPointCloud2ToPointCloud(*cloud_msg, out_cloud);

	//ROS pointcloud zu pcl pointcloud konvertieren
	pcl::PCLPointCloud2 pcl_pc2;
	pcl_conversions::toPCL(*cloud_msg,pcl_pc2);
	pcl::PointCloud<pcl::PointXYZ>::Ptr temp_cloud(new pcl::PointCloud<pcl::PointXYZ>);
	pcl::fromPCLPointCloud2(pcl_pc2,*temp_cloud);

	//Daten in Datei speichern
	FilePtr = fopen("Data.txt", "a");
	fprintf(FilePtr, "Cloud: width = %d, height = %d\n", cloud_msg->width, cloud_msg->height);

	//Minimum Z-Wert bestimmen
	pcl::PointXYZ minPt, maxPt;
	pcl::getMinMax3D(*temp_cloud, minPt, maxPt);
	fprintf(FilePtr, cloud_msg->header.frame_id.c_str());
	fprintf(FilePtr, "\nMin Z Value: %f)\n", minPt.z);
	fprintf(FilePtr, "######################################\n");
	
	//allocate lateral distance array dynamically
	//lat_dist = new double[cloud_msg->width * cloud_msg->height];

	//save data to file
	fprintf(FilePtr, "Data\n");
	int i=0;
	BOOST_FOREACH (const geometry_msgs::Point32 pt, out_cloud.points) {
		alpha_XY = atan(abs(pt.z/pt.y));
		if (pt.y < 0)
			gamma = alpha_XY + geo_angl_XY;
		else
			gamma = alpha_XY - geo_angl_XY;       	
		lat_dist.push_back((sqrt(pow(pt.z,2)+pow(pt.y,2))+geo_dist_Y*cos(geo_angl_XY))*sin(gamma));
		fprintf (FilePtr, "%f\n%f, %f, %f\nalpha = %f, gamma = %f, geo_angle = %f\n", lat_dist[i], pt.x, pt.y, pt.z, alpha_XY, gamma, geo_angl_XY);
		i++;
	}

	//Determining minimal lateral distance to camera
	double min_lat_dist = *std::min_element(std::begin(lat_dist), std::end(lat_dist));
	if (min_lat_dist < 1) {
		min_lat_dist = 1;
		}
	close_obst = min_lat_dist;

	//Determining required flight speed
	double	v_fwd = min_lat_dist * speed_prop;

	fprintf(FilePtr, "min value: %lf\n", min_lat_dist);
	fail=fprintf(FilePtr, "######################################\n");
	ROS_INFO("inside callback");
	printf("%d\n", fail);
	ferror(FilePtr);	

	sleep(50000);
	fclose(FilePtr);
}

int main(int argc, char** argv) {
	try { std::remove ("Data.txt"); } catch(...) {};
	ros::init (argc, argv, "pointcloud_test");	
	sensor_msgs::PointCloud2 input_cloud;
	
	ros::NodeHandle nh1, nh2, nh3;	
	ros::Subscriber sub1, sub2, sub3;

	ROS_INFO("pointcloud_test started");
	sub1 = nh1.subscribe ("/camera_front/depth/points", 1, cloud_callback);
	sub2 = nh2.subscribe ("/camera_left/depth/points", 1, cloud_callback);
	sub3 = nh3.subscribe ("/camera_right/depth/points", 1, cloud_callback);
	//ROS_INFO("%lf\n", sub2);
	ros::spin();

	return 0;
}


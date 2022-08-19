#! /bin/bash

catkin_ws="$1"
gazebo="$2"
px4="$3"
env="$4"

echo "building DeepPX4 ..."
# exit when any command fails
set -e

# move custom HANNASCAPES gazebo models
if [ ! -d "$gazebo" ]; then
	echo "$gazebo not found, did you install gazebo?"
	exit 125
fi

mkdir -p "$gazebo/models"
cp -r HANNAS_ground_plane "$gazebo/models"
cp -r HANNAS_wall "$gazebo/models"

# move custom HANNAS camera to px4
if [ ! -d "$px4" ]; then
	echo "$px4 not found, did you install px4?"
	exit 125
fi

cp -r HANNAS_iris_triple_depth_camera "$px4/Tools/sitl_gazebo/models"

# move HANNASCAPES worlds to local planner of avoidance
if [ ! -d "$catkin_ws/src/avoidance" ]; then
	echo "avoidance not found, did you install avoidace and local_planner as instructed?"
	exit 125
fi
cp -r launch/HANNASSCAPES "$catkin_ws/src/avoidance/local_planner/launch"
cp -r worlds/HANNASSCAPES "$catkin_ws/src/avoidance/avoidance/sim/worlds"

echo "export to bashrc script"

. "$px4"/Tools/setup_gazebo.bash ~/"$px4" ~/"$px4"/build/px4_sitl_default >> ~/.bashrc 
export ROS_PACKAGE_PATH=${ROS_PACKAGE_PATH}:~/"$px4" >> ~/.bashrc 
export GAZEBO_MODEL_PATH=${GAZEBO_MODEL_PATH}:~/"$catkin_ws"/src/avoidance/avoidance/sim/models:"$gazebo":./gazebo/models:~/"$px4"/Tools/sitl_gazebo/models:~/"$catkin_ws"/src/avoidance/avoidance/sim/models:./gazebo/models:~/.gazebo/models:~/"$px4"/Tools/sitl_gazebo/models:~/"$catkin_ws"/src/avoidance/avoidance/sim/models:~/"$catkin_ws"/src/avoidance/avoidance/sim/worlds >> ~/.bashrc 
export GAZEBO_RESOURCE_PATH=${GAZEBO_RESOURCE_PATH}:/home/"xqsme"/"$catkin_ws"/src/avoidance/avoidance/sim/worlds/HANNASSCAPES >> ~/.bashrc 

if [ ! -z "$env" ]
then
	echo "creating conda environment"
	conda create --name "$env" python=3.8
	conda activate "$env"
	pip install -r requirements.txt
	~/anaconda3/envs/"$env"/bin/python -m pip install paddlepaddle==2.3.1 -i https://mirror.baidu.com/pypi/simple
	pip install paddleseg
fi

echo "DeepPX4 build successfull"

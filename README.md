# DeepPX4
ROS implementation of PX4 + Semantic Segmentation for PX4 cost function look up table (LUT)
# AUTHORS  
Luc Stiemer (FH Aachen, University of Applied Science, luc.stiemer@alumni.fh-aachen.de)  
Andreas Thoma (FH Aachen, University of Applied Science)  
Carsten Braun (FH Aachen, University of Applied Science)

# INTRODUCTION
DeepPX4 is a PX4 implementation with a segmentation based Parameter Tuner to make the PX4 local planner more efficient.  
The front cameras rgb image is used for segmentation based on the ppliteseg model trained and implemented in (PaddlePaddle) paddleseg. The model  
is trained on four classes: Buildings, Road, Sky, Trees. However, you can train your own model and implement it here as well. Further, we have a  
repo for gazebo custom dataset creation if you want more or other classes (https://github.com/xQsM3/Gazebo-Segmentation-Dataset-Creator). The  
segmentation is used to suggest tuned parameters which are then published to the local planner dynamic reconfigure service. Right now we are testing  
different algorithms for the parameter suggestion, e.g. different parameters depending on whether the drone flies through a big city / small city /  
vegetation, or determining whether the drone is flying above a road parallel to road vector. 

# INSTALLATION

## install ros + px4 + gazebo noetic (however this is also tested on melodic)  
sudo apt update  
sudo apt upgrade  
sudo apt install git  
mkdir src  
cd src  
git clone https://github.com/PX4/Firmware.git --recursive  
cd Firmware  
bash ./Tools/setup/ubuntu.sh  

## reboot computer
wget https://raw.githubusercontent.com/ktelegenov/sim_ros_setup_noetic/main/ubuntu_sim_ros_noetic.sh  
bash ubuntu_sim_ros_noetic.sh  

## close the terminal and open it again
cd src/Firmware  
git submodule update --init --recursive  
DONT_RUN=1 make px4_sitl_default gazebo  
  
source Tools/setup_gazebo.bash $(pwd) $(pwd)/build/px4_sitl_default  
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd):$(pwd)/Tools/sitl_gazebo  
  
roslaunch px4 multi_uav_mavros_sitl.launch  

## install px4 avoidance
cd ~/catkin_ws/src  
  
follow  install instructions  
https://github.com/PX4/PX4-Avoidance  

## install anaconda
https://docs.anaconda.com/anaconda/install/  

## install DeepPX4
cd  
git clone https://github.com/xQsM3/DeepPX4.git  
cd ~/DeepPX4/build_DeepPX4  

now build DeepPX4 and create a conda environment with paddleseg cpu version with the following bash. If you have a CUDA  
GPU you can leave the [env] argument empty and build your own conda environment by following  
https://github.com/PaddlePaddle/PaddleSeg/blob/release/2.6/docs/install.md  
  
bash build.sh [catkin_ws] [gazebo] [px4] [env]  
e.g.:  
bash build.sh ~/catkin_ws ~/.gazebo ~/Firmware paddleseg_cpu  #change FIrmware path to your path


cd ~/DeepPX4  
catkin_make  
source devel/setup.bash  

# USAGE
## start multiple worlds  
cd ~/DeepPx4 ./px4_sim_script_all_worlds_HANNASSCAPES all  


  
## start single world  
1) terminal  
cd ~/catkin_ws  
catkin build -w ~/catkin_ws # if not build yet  
source ~/catkin_ws/devel/setup.bash  
cd ~/Firmware  # change this if you install firmware somewhere else
source Tools/setup_gazebo.bash $(pwd) $(pwd)/build/px4_sitl_default  
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd):$(pwd)/Tools/sitl_gazebo  
roslaunch local_planner HANNASSCAPES_city_obst_1.launch #run a world    
rosrun mavros mavsys mode -c OFFBOARD; rosrun mavros mavsafety arm
2) terminal  
cd ~/DeepPX4  
conda activate paddleseg_cpu # if working with virtual environment  
catkin_make  
source devel/setup.bash  
cd ~/DeepPX4/src/Parameter_Tuning/scripts/  
python parameter_tuner.py  

  
# DEBUG WITH PYCHARM  
https://www.youtube.com/watch?v=lTew9mbXrAs&t=288s  
debug with pycharm:  
cd ~/DeepPX4/src  
source venv/bin/activate  
cd ..  
catkin_make  
source devel/setup.bash  
pycharm-community  

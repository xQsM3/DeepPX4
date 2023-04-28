/*
Function to control the value of control parameters of the px4 avoid
Written by: Andreas Thoma
Last edited: 7.04.21
*/
#include <local_planner/communication_controller.h>

namespace avoidance {
void communication_controller_fun(std::string para_name, int para_value) {
  dynamic_reconfigure::ReconfigureRequest srv_req;
  dynamic_reconfigure::ReconfigureResponse srv_resp;
  dynamic_reconfigure::DoubleParameter param;
  dynamic_reconfigure::Config conf;

  param.name = para_name;
  param.value = para_value;
  conf.doubles.push_back(param);

  srv_req.config = conf;

  if (ros::service::call("/local_planner_nodelet/set_parameters", srv_req, srv_resp)) {
    ROS_INFO("call to set local_planner parameters succeeded");
  } else {
    ROS_INFO("call to set local_planner parameters failed");
  }

}

/* int main(int argc, char **argv) {
  ros::init(argc, argv, "communication_controller");

  communication_controller_fun("goal_z_param", 8);


  return 0;
} */
}


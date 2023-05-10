//library for communication_controller
#include <dynamic_reconfigure/DoubleParameter.h>
#include <dynamic_reconfigure/Reconfigure.h>
#include <dynamic_reconfigure/Config.h>
#include <ros/ros.h>

namespace avoidance {

class communication_controller{
public:
  int counter = 0;
  /**
  * @brief	dynamically reconfigures the px4 avoid control parameter given by para_name with value para_value
  **/
  void communication_controller_fun(std::string para_name, int para_value) const;
};
}

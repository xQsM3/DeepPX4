# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "segmentation: 1 messages, 1 services")

set(MSG_I_FLAGS "-Isegmentation:/home/xqsme/DeepPX4/src/segmentation/msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg;-Isensor_msgs:/opt/ros/noetic/share/sensor_msgs/cmake/../msg;-Isegmentation:/home/xqsme/DeepPX4/src/segmentation/msg;-Igeometry_msgs:/opt/ros/noetic/share/geometry_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(segmentation_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg" NAME_WE)
add_custom_target(_segmentation_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "segmentation" "/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg" "sensor_msgs/CameraInfo:sensor_msgs/Image:std_msgs/Header:sensor_msgs/RegionOfInterest"
)

get_filename_component(_filename "/home/xqsme/DeepPX4/src/segmentation/srv/Segmentation.srv" NAME_WE)
add_custom_target(_segmentation_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "segmentation" "/home/xqsme/DeepPX4/src/segmentation/srv/Segmentation.srv" "sensor_msgs/RegionOfInterest:sensor_msgs/CameraInfo:std_msgs/Header:segmentation/SegImage:sensor_msgs/Image"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(segmentation
  "/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/CameraInfo.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/RegionOfInterest.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/segmentation
)

### Generating Services
_generate_srv_cpp(segmentation
  "/home/xqsme/DeepPX4/src/segmentation/srv/Segmentation.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/RegionOfInterest.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/CameraInfo.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/segmentation
)

### Generating Module File
_generate_module_cpp(segmentation
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/segmentation
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(segmentation_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(segmentation_generate_messages segmentation_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg" NAME_WE)
add_dependencies(segmentation_generate_messages_cpp _segmentation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/xqsme/DeepPX4/src/segmentation/srv/Segmentation.srv" NAME_WE)
add_dependencies(segmentation_generate_messages_cpp _segmentation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(segmentation_gencpp)
add_dependencies(segmentation_gencpp segmentation_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS segmentation_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(segmentation
  "/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/CameraInfo.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/RegionOfInterest.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/segmentation
)

### Generating Services
_generate_srv_eus(segmentation
  "/home/xqsme/DeepPX4/src/segmentation/srv/Segmentation.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/RegionOfInterest.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/CameraInfo.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/segmentation
)

### Generating Module File
_generate_module_eus(segmentation
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/segmentation
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(segmentation_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(segmentation_generate_messages segmentation_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg" NAME_WE)
add_dependencies(segmentation_generate_messages_eus _segmentation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/xqsme/DeepPX4/src/segmentation/srv/Segmentation.srv" NAME_WE)
add_dependencies(segmentation_generate_messages_eus _segmentation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(segmentation_geneus)
add_dependencies(segmentation_geneus segmentation_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS segmentation_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(segmentation
  "/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/CameraInfo.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/RegionOfInterest.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/segmentation
)

### Generating Services
_generate_srv_lisp(segmentation
  "/home/xqsme/DeepPX4/src/segmentation/srv/Segmentation.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/RegionOfInterest.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/CameraInfo.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/segmentation
)

### Generating Module File
_generate_module_lisp(segmentation
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/segmentation
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(segmentation_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(segmentation_generate_messages segmentation_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg" NAME_WE)
add_dependencies(segmentation_generate_messages_lisp _segmentation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/xqsme/DeepPX4/src/segmentation/srv/Segmentation.srv" NAME_WE)
add_dependencies(segmentation_generate_messages_lisp _segmentation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(segmentation_genlisp)
add_dependencies(segmentation_genlisp segmentation_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS segmentation_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(segmentation
  "/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/CameraInfo.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/RegionOfInterest.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/segmentation
)

### Generating Services
_generate_srv_nodejs(segmentation
  "/home/xqsme/DeepPX4/src/segmentation/srv/Segmentation.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/RegionOfInterest.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/CameraInfo.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/segmentation
)

### Generating Module File
_generate_module_nodejs(segmentation
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/segmentation
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(segmentation_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(segmentation_generate_messages segmentation_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg" NAME_WE)
add_dependencies(segmentation_generate_messages_nodejs _segmentation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/xqsme/DeepPX4/src/segmentation/srv/Segmentation.srv" NAME_WE)
add_dependencies(segmentation_generate_messages_nodejs _segmentation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(segmentation_gennodejs)
add_dependencies(segmentation_gennodejs segmentation_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS segmentation_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(segmentation
  "/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/CameraInfo.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/RegionOfInterest.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/segmentation
)

### Generating Services
_generate_srv_py(segmentation
  "/home/xqsme/DeepPX4/src/segmentation/srv/Segmentation.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/RegionOfInterest.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/CameraInfo.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/segmentation
)

### Generating Module File
_generate_module_py(segmentation
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/segmentation
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(segmentation_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(segmentation_generate_messages segmentation_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/xqsme/DeepPX4/src/segmentation/msg/SegImage.msg" NAME_WE)
add_dependencies(segmentation_generate_messages_py _segmentation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/xqsme/DeepPX4/src/segmentation/srv/Segmentation.srv" NAME_WE)
add_dependencies(segmentation_generate_messages_py _segmentation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(segmentation_genpy)
add_dependencies(segmentation_genpy segmentation_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS segmentation_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/segmentation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/segmentation
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(segmentation_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET sensor_msgs_generate_messages_cpp)
  add_dependencies(segmentation_generate_messages_cpp sensor_msgs_generate_messages_cpp)
endif()
if(TARGET segmentation_generate_messages_cpp)
  add_dependencies(segmentation_generate_messages_cpp segmentation_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/segmentation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/segmentation
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(segmentation_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET sensor_msgs_generate_messages_eus)
  add_dependencies(segmentation_generate_messages_eus sensor_msgs_generate_messages_eus)
endif()
if(TARGET segmentation_generate_messages_eus)
  add_dependencies(segmentation_generate_messages_eus segmentation_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/segmentation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/segmentation
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(segmentation_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET sensor_msgs_generate_messages_lisp)
  add_dependencies(segmentation_generate_messages_lisp sensor_msgs_generate_messages_lisp)
endif()
if(TARGET segmentation_generate_messages_lisp)
  add_dependencies(segmentation_generate_messages_lisp segmentation_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/segmentation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/segmentation
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(segmentation_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET sensor_msgs_generate_messages_nodejs)
  add_dependencies(segmentation_generate_messages_nodejs sensor_msgs_generate_messages_nodejs)
endif()
if(TARGET segmentation_generate_messages_nodejs)
  add_dependencies(segmentation_generate_messages_nodejs segmentation_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/segmentation)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/segmentation\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/segmentation
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(segmentation_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET sensor_msgs_generate_messages_py)
  add_dependencies(segmentation_generate_messages_py sensor_msgs_generate_messages_py)
endif()
if(TARGET segmentation_generate_messages_py)
  add_dependencies(segmentation_generate_messages_py segmentation_generate_messages_py)
endif()

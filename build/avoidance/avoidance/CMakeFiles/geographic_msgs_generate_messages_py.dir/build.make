# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/xqsme/DeepPX4/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/xqsme/DeepPX4/build

# Utility rule file for geographic_msgs_generate_messages_py.

# Include the progress variables for this target.
include avoidance/avoidance/CMakeFiles/geographic_msgs_generate_messages_py.dir/progress.make

geographic_msgs_generate_messages_py: avoidance/avoidance/CMakeFiles/geographic_msgs_generate_messages_py.dir/build.make

.PHONY : geographic_msgs_generate_messages_py

# Rule to build all files generated by this target.
avoidance/avoidance/CMakeFiles/geographic_msgs_generate_messages_py.dir/build: geographic_msgs_generate_messages_py

.PHONY : avoidance/avoidance/CMakeFiles/geographic_msgs_generate_messages_py.dir/build

avoidance/avoidance/CMakeFiles/geographic_msgs_generate_messages_py.dir/clean:
	cd /home/xqsme/DeepPX4/build/avoidance/avoidance && $(CMAKE_COMMAND) -P CMakeFiles/geographic_msgs_generate_messages_py.dir/cmake_clean.cmake
.PHONY : avoidance/avoidance/CMakeFiles/geographic_msgs_generate_messages_py.dir/clean

avoidance/avoidance/CMakeFiles/geographic_msgs_generate_messages_py.dir/depend:
	cd /home/xqsme/DeepPX4/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/xqsme/DeepPX4/src /home/xqsme/DeepPX4/src/avoidance/avoidance /home/xqsme/DeepPX4/build /home/xqsme/DeepPX4/build/avoidance/avoidance /home/xqsme/DeepPX4/build/avoidance/avoidance/CMakeFiles/geographic_msgs_generate_messages_py.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : avoidance/avoidance/CMakeFiles/geographic_msgs_generate_messages_py.dir/depend


# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.27

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
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
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/DaniilPC/POOSE/BSE/server

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/DaniilPC/POOSE/BSE/server/build

# Include any dependencies generated for this target.
include CMakeFiles/BSE.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/BSE.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/BSE.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/BSE.dir/flags.make

CMakeFiles/BSE.dir/extra/python_bindings.cpp.o: CMakeFiles/BSE.dir/flags.make
CMakeFiles/BSE.dir/extra/python_bindings.cpp.o: /home/DaniilPC/POOSE/BSE/server/extra/python_bindings.cpp
CMakeFiles/BSE.dir/extra/python_bindings.cpp.o: CMakeFiles/BSE.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/DaniilPC/POOSE/BSE/server/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/BSE.dir/extra/python_bindings.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/BSE.dir/extra/python_bindings.cpp.o -MF CMakeFiles/BSE.dir/extra/python_bindings.cpp.o.d -o CMakeFiles/BSE.dir/extra/python_bindings.cpp.o -c /home/DaniilPC/POOSE/BSE/server/extra/python_bindings.cpp

CMakeFiles/BSE.dir/extra/python_bindings.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/BSE.dir/extra/python_bindings.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/DaniilPC/POOSE/BSE/server/extra/python_bindings.cpp > CMakeFiles/BSE.dir/extra/python_bindings.cpp.i

CMakeFiles/BSE.dir/extra/python_bindings.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/BSE.dir/extra/python_bindings.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/DaniilPC/POOSE/BSE/server/extra/python_bindings.cpp -o CMakeFiles/BSE.dir/extra/python_bindings.cpp.s

# Object files for target BSE
BSE_OBJECTS = \
"CMakeFiles/BSE.dir/extra/python_bindings.cpp.o"

# External object files for target BSE
BSE_EXTERNAL_OBJECTS =

BSE.cpython-312-x86_64-linux-gnu.so: CMakeFiles/BSE.dir/extra/python_bindings.cpp.o
BSE.cpython-312-x86_64-linux-gnu.so: CMakeFiles/BSE.dir/build.make
BSE.cpython-312-x86_64-linux-gnu.so: CMakeFiles/BSE.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/home/DaniilPC/POOSE/BSE/server/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared module BSE.cpython-312-x86_64-linux-gnu.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/BSE.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/BSE.dir/build: BSE.cpython-312-x86_64-linux-gnu.so
.PHONY : CMakeFiles/BSE.dir/build

CMakeFiles/BSE.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/BSE.dir/cmake_clean.cmake
.PHONY : CMakeFiles/BSE.dir/clean

CMakeFiles/BSE.dir/depend:
	cd /home/DaniilPC/POOSE/BSE/server/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/DaniilPC/POOSE/BSE/server /home/DaniilPC/POOSE/BSE/server /home/DaniilPC/POOSE/BSE/server/build /home/DaniilPC/POOSE/BSE/server/build /home/DaniilPC/POOSE/BSE/server/build/CMakeFiles/BSE.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/BSE.dir/depend


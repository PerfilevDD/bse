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
include CMakeFiles/BSM.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/BSM.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/BSM.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/BSM.dir/flags.make

CMakeFiles/BSM.dir/extra/python_bindings.cpp.o: CMakeFiles/BSM.dir/flags.make
CMakeFiles/BSM.dir/extra/python_bindings.cpp.o: /home/DaniilPC/POOSE/BSE/server/extra/python_bindings.cpp
CMakeFiles/BSM.dir/extra/python_bindings.cpp.o: CMakeFiles/BSM.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/DaniilPC/POOSE/BSE/server/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/BSM.dir/extra/python_bindings.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/BSM.dir/extra/python_bindings.cpp.o -MF CMakeFiles/BSM.dir/extra/python_bindings.cpp.o.d -o CMakeFiles/BSM.dir/extra/python_bindings.cpp.o -c /home/DaniilPC/POOSE/BSE/server/extra/python_bindings.cpp

CMakeFiles/BSM.dir/extra/python_bindings.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/BSM.dir/extra/python_bindings.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/DaniilPC/POOSE/BSE/server/extra/python_bindings.cpp > CMakeFiles/BSM.dir/extra/python_bindings.cpp.i

CMakeFiles/BSM.dir/extra/python_bindings.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/BSM.dir/extra/python_bindings.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/DaniilPC/POOSE/BSE/server/extra/python_bindings.cpp -o CMakeFiles/BSM.dir/extra/python_bindings.cpp.s

CMakeFiles/BSM.dir/src/asset/Asset.cpp.o: CMakeFiles/BSM.dir/flags.make
CMakeFiles/BSM.dir/src/asset/Asset.cpp.o: /home/DaniilPC/POOSE/BSE/server/src/asset/Asset.cpp
CMakeFiles/BSM.dir/src/asset/Asset.cpp.o: CMakeFiles/BSM.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/DaniilPC/POOSE/BSE/server/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/BSM.dir/src/asset/Asset.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/BSM.dir/src/asset/Asset.cpp.o -MF CMakeFiles/BSM.dir/src/asset/Asset.cpp.o.d -o CMakeFiles/BSM.dir/src/asset/Asset.cpp.o -c /home/DaniilPC/POOSE/BSE/server/src/asset/Asset.cpp

CMakeFiles/BSM.dir/src/asset/Asset.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/BSM.dir/src/asset/Asset.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/DaniilPC/POOSE/BSE/server/src/asset/Asset.cpp > CMakeFiles/BSM.dir/src/asset/Asset.cpp.i

CMakeFiles/BSM.dir/src/asset/Asset.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/BSM.dir/src/asset/Asset.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/DaniilPC/POOSE/BSE/server/src/asset/Asset.cpp -o CMakeFiles/BSM.dir/src/asset/Asset.cpp.s

CMakeFiles/BSM.dir/src/marketplace/Marketplace.cpp.o: CMakeFiles/BSM.dir/flags.make
CMakeFiles/BSM.dir/src/marketplace/Marketplace.cpp.o: /home/DaniilPC/POOSE/BSE/server/src/marketplace/Marketplace.cpp
CMakeFiles/BSM.dir/src/marketplace/Marketplace.cpp.o: CMakeFiles/BSM.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/DaniilPC/POOSE/BSE/server/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/BSM.dir/src/marketplace/Marketplace.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/BSM.dir/src/marketplace/Marketplace.cpp.o -MF CMakeFiles/BSM.dir/src/marketplace/Marketplace.cpp.o.d -o CMakeFiles/BSM.dir/src/marketplace/Marketplace.cpp.o -c /home/DaniilPC/POOSE/BSE/server/src/marketplace/Marketplace.cpp

CMakeFiles/BSM.dir/src/marketplace/Marketplace.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/BSM.dir/src/marketplace/Marketplace.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/DaniilPC/POOSE/BSE/server/src/marketplace/Marketplace.cpp > CMakeFiles/BSM.dir/src/marketplace/Marketplace.cpp.i

CMakeFiles/BSM.dir/src/marketplace/Marketplace.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/BSM.dir/src/marketplace/Marketplace.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/DaniilPC/POOSE/BSE/server/src/marketplace/Marketplace.cpp -o CMakeFiles/BSM.dir/src/marketplace/Marketplace.cpp.s

CMakeFiles/BSM.dir/src/user/User.cpp.o: CMakeFiles/BSM.dir/flags.make
CMakeFiles/BSM.dir/src/user/User.cpp.o: /home/DaniilPC/POOSE/BSE/server/src/user/User.cpp
CMakeFiles/BSM.dir/src/user/User.cpp.o: CMakeFiles/BSM.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/DaniilPC/POOSE/BSE/server/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object CMakeFiles/BSM.dir/src/user/User.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/BSM.dir/src/user/User.cpp.o -MF CMakeFiles/BSM.dir/src/user/User.cpp.o.d -o CMakeFiles/BSM.dir/src/user/User.cpp.o -c /home/DaniilPC/POOSE/BSE/server/src/user/User.cpp

CMakeFiles/BSM.dir/src/user/User.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/BSM.dir/src/user/User.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/DaniilPC/POOSE/BSE/server/src/user/User.cpp > CMakeFiles/BSM.dir/src/user/User.cpp.i

CMakeFiles/BSM.dir/src/user/User.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/BSM.dir/src/user/User.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/DaniilPC/POOSE/BSE/server/src/user/User.cpp -o CMakeFiles/BSM.dir/src/user/User.cpp.s

# Object files for target BSM
BSM_OBJECTS = \
"CMakeFiles/BSM.dir/extra/python_bindings.cpp.o" \
"CMakeFiles/BSM.dir/src/asset/Asset.cpp.o" \
"CMakeFiles/BSM.dir/src/marketplace/Marketplace.cpp.o" \
"CMakeFiles/BSM.dir/src/user/User.cpp.o"

# External object files for target BSM
BSM_EXTERNAL_OBJECTS =

BSM.cpython-312-x86_64-linux-gnu.so: CMakeFiles/BSM.dir/extra/python_bindings.cpp.o
BSM.cpython-312-x86_64-linux-gnu.so: CMakeFiles/BSM.dir/src/asset/Asset.cpp.o
BSM.cpython-312-x86_64-linux-gnu.so: CMakeFiles/BSM.dir/src/marketplace/Marketplace.cpp.o
BSM.cpython-312-x86_64-linux-gnu.so: CMakeFiles/BSM.dir/src/user/User.cpp.o
BSM.cpython-312-x86_64-linux-gnu.so: CMakeFiles/BSM.dir/build.make
BSM.cpython-312-x86_64-linux-gnu.so: CMakeFiles/BSM.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/home/DaniilPC/POOSE/BSE/server/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Linking CXX shared module BSM.cpython-312-x86_64-linux-gnu.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/BSM.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/BSM.dir/build: BSM.cpython-312-x86_64-linux-gnu.so
.PHONY : CMakeFiles/BSM.dir/build

CMakeFiles/BSM.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/BSM.dir/cmake_clean.cmake
.PHONY : CMakeFiles/BSM.dir/clean

CMakeFiles/BSM.dir/depend:
	cd /home/DaniilPC/POOSE/BSE/server/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/DaniilPC/POOSE/BSE/server /home/DaniilPC/POOSE/BSE/server /home/DaniilPC/POOSE/BSE/server/build /home/DaniilPC/POOSE/BSE/server/build /home/DaniilPC/POOSE/BSE/server/build/CMakeFiles/BSM.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/BSM.dir/depend


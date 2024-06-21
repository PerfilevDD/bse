#----------------------------------------------#
#-----Konfiguration des Buildsystems CMake-----#
#----------------------------------------------#

# Minimale Version des Buildsystems
cmake_minimum_required(VERSION 3.16)
# Name des Projekts
project(BSE)


#----------------------------------------------#
#-------------------Optionen-------------------#
#----------------------------------------------#

# Setzte verwendeten C++-Standard auf C++17
set(CMAKE_CXX_STANDARD 17)
# Optional: Baue mit Debugsymbolen / Optimierung
set(CMAKE_BUILD_TYPE Debug)
# set(CMAKE_BUILD_TYPE Release)
# Optional: Prüfe alle Targets auf Speicherlecks
# add_compile_options(-fsanitize=address)
# add_link_options(-fsanitize=address)

# Füge Includeverzeichnisse hinzu
include_directories(include)
include_directories(external)



#----------------------------------------------#
#----------Download and use GoogleTest---------#
#----------------------------------------------#

# Use CMakes FetchContent
include(FetchContent)
# Workaround for CMake >= 3.24
# Avoid warning about DOWNLOAD_EXTRACT_TIMESTAMP
if (CMAKE_VERSION VERSION_GREATER_EQUAL "3.24.0")
  cmake_policy(SET CMP0135 NEW)
endif()

# Download GoogleTest (we use version 1.12.1)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# Workaround for Windows:
# Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

# GoogleTest soll nur lokal, in diesem Projekt verwendet werden.
option(INSTALL_GTEST "Enable installation of googletest." OFF)

# Include CMake configuration of GoogleTest
FetchContent_MakeAvailable(googletest)
include(GoogleTest)

# Enable GoogleTest
enable_testing()



#----------------------------------------------#
#----------Download and use pybind11-----------#
#----------------------------------------------#

# Download pybind11
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG v2.10.4
)

# Include pybind11
FetchContent_MakeAvailable(pybind11)

#----------------------------------------------#
#----------Download and use sqlpp1-----------#
#----------------------------------------------#

# Download pybind11
FetchContent_Declare(
        sqlpp11
        GIT_REPOSITORY https://github.com/rbock/sqlpp11.git
        GIT_TAG main
)

# Include sqlpp11
set(BUILD_SQLITE3_CONNECTOR ON)
FetchContent_MakeAvailable(sqlpp11)


#----------------------------------------------#
#-----------------Add Matplot++----------------#
#----------------------------------------------#
FetchContent_Declare(matplotplusplus
        GIT_REPOSITORY https://github.com/alandefreitas/matplotplusplus
        GIT_TAG origin/master)

FetchContent_GetProperties(matplotplusplus)
if(NOT matplotplusplus_POPULATED)
  FetchContent_Populate(matplotplusplus)
  add_subdirectory(${matplotplusplus_SOURCE_DIR} ${matplotplusplus_BINARY_DIR} EXCLUDE_FROM_ALL)
endif()



#----------------------------------------------#
#---------------Erzeuge Projekt----------------#
#----------------------------------------------#

# Legt die Variable SRC_FILES an, die alle
# .cpp-Dateien des Projekts benennt,
# die in Verzeichnis src/ liegen.
file(GLOB SRC_FILES
  ${PROJECT_SOURCE_DIR}/src/*.cpp
  ${PROJECT_SOURCE_DIR}/src/asset/*.cpp
  ${PROJECT_SOURCE_DIR}/src/db/*.cpp
  ${PROJECT_SOURCE_DIR}/src/marketplace/*.cpp
  ${PROJECT_SOURCE_DIR}/src/user/*.cpp
        )


# Baue das Programm '---' aus den Quellen
file(GLOB SRC_FILES
${PROJECT_SOURCE_DIR}/src/*.cpp
${PROJECT_SOURCE_DIR}/src/db/*.cpp
${PROJECT_SOURCE_DIR}/src/asset/*.cpp
${PROJECT_SOURCE_DIR}/src/marketplace/*.cpp
${PROJECT_SOURCE_DIR}/src/user/*.cpp)


pybind11_add_module(BSE
  extra/python_bindings.cpp
  ${SRC_FILES}
)

# Installiere Pythonmodul im Verzeichnis '---'
install(TARGETS BSE
  COMPONENT python
  LIBRARY DESTINATION ${PROJECT_SOURCE_DIR}/extra)



target_link_libraries(BSE PRIVATE sqlpp11::sqlpp11)

target_link_libraries(BSE PRIVATE sqlpp11::sqlite3)


#----------------------------------------------#
#-------------Erzeuge Testprogramme------------#
#----------------------------------------------#

file(GLOB SRC_FILES ${PROJECT_SOURCE_DIR}/src/*.cpp)
add_executable(test_database tests/test_database.cpp ${SRC_FILES}
        src/db/sqlite.cpp
        src/user/User.cpp)
target_link_libraries(test_database GTest::gtest_main)
target_link_libraries(test_database sqlite3)
target_link_libraries(test_database sqlpp11)
gtest_discover_tests(test_database)

#add_executable(main src/main.cpp)
#target_link_libraries(main PUBLIC matplot)

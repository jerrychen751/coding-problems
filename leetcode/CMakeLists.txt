# Works both standalone and as a subdirectory of the repo root.
if(CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
    cmake_minimum_required(VERSION 3.20)
    project(LeetCode LANGUAGES CXX)

    set(CMAKE_CXX_STANDARD 23)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/outputs")
file(MAKE_DIRECTORY "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")

get_filename_component(DIR_PREFIX "${CMAKE_CURRENT_SOURCE_DIR}" NAME)
file(GLOB SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")

foreach(SOURCE_FILE IN LISTS SOURCES)
    file(READ "${SOURCE_FILE}" SOURCE_CONTENT)
    if(NOT SOURCE_CONTENT MATCHES "int[ \t\r\n]+main[ \t\r\n]*\\(")
        continue()
    endif()

    get_filename_component(EXECUTABLE_BASENAME "${SOURCE_FILE}" NAME_WE)
    set(TARGET_NAME "${DIR_PREFIX}__${EXECUTABLE_BASENAME}")

    add_executable("${TARGET_NAME}" "${SOURCE_FILE}")
    set_target_properties("${TARGET_NAME}" PROPERTIES OUTPUT_NAME "${EXECUTABLE_BASENAME}")
endforeach()

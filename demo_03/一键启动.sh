#!/usr/bin/env bash
#source环境变量
source /home/intel/ros_voice_system/devel/setup.bash
gnome-terminal -t "启动rbcBot机器人" -x bash -c "roslaunch mx_bringup rbc_lidar_start.launch ;"
sleep 2.5
gnome-terminal -t "启动amcl导航" -x bash -c "roslaunch mx_nav amcl_demo.launch ;"
sleep 1
# 启动movidius脚本
gnome-terminal -x bash -c "roslaunch realsense_camera r200_nodelet_rgbd.launch"
sleep 1
gnome-terminal -x bash -c "roslaunch movidius_ncs_launch ncs_camera.launch cnn_type:=mobilenetssd camera:=others input_topic:=/camera/rgb/image_raw "
sleep 1
gnome-terminal -x bash -c "roslaunch movidius_ncs_launch ncs_stream_detection_example.launch camera_topic:=/camera/rgb/image_raw "

sleep 1
#启动识别播报脚本
gnome-terminal -x bash -c " python ~/Desktop/wrc_demo/demo_03/objectSearch.py "
sleep 1
gnome-terminal -x bash -c " python ~/Desktop/wrc_demo/demo_03/sendGoals.py "

#!/bin/bash

killall gnome-terminal-server
source /home/intel/ros_voice_system/devel/setup.bash;

gnome-terminal -t "启动rbcBot机器人" -x bash -c "roslaunch mx_bringup rbc_lidar_start.launch ;"

sleep 2.5
gnome-terminal -t "启动amcl导航" -x bash -c "roslaunch mx_nav amcl_demo.launch ;"
sleep 5
gnome-terminal -t "启动二维码识别" -x bash -c " python ~/Desktop/wrc_demo/demo_02/qrcodeNav.py ;"
sleep 2
gnome-terminal -t "启动amcl" -x bash -c "roslaunch mx_rviz amcl_view.launch ;"
sleep 1
gnome-terminal -t "发送导航坐标" -x bash -c " python ~/Desktop/wrc_demo/demo_02/sendGoals.py  ;"


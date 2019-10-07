#!/usr/bin/env python
# -*- coding: utf-8 -*-
#物品检测相关
import rospy,os
from std_msgs.msg import String
from object_msgs.msg import ObjectsInBoxes

#回调函数
ob_flag = 0
def callback(data):
    global ob_flag 
    data = data.objects_vector
    pub = rospy.Publisher('wrc_objects', String, queue_size=10)
    rate = rospy.Rate(10) # 10hz 
    log_txt = open("/home/intel/Desktop/log.txt","a")  
    if data:        
        for i in data:
            p = i.object.probability
            object_name = i.object.object_name
            if p >= 0.978:
                if object_name == 'cat' and ob_flag != 1:#已测试
                    os.system("play ~/Desktop/wrc_demo/wrc_file/cat.mp3 ")
                    ob_flag = 1
                elif object_name == 'dog' and ob_flag != 2:#        准备放弃×××
                    
                    print('狗')
                    ob_flag = 2
                elif object_name == 'bottle'and ob_flag != 3:#已测试.
                    os.system('play ~/Desktop/wrc_demo/wrc_file/bottle.mp3 ')
                    print('瓶子')
                    ob_flag = 3
                elif object_name == 'tvmonitor'and ob_flag != 4:#已测试
                    os.system("play ~/Desktop/wrc_demo/wrc_file/TV.mp3 ")
                    print('电视机')
                    ob_flag = 4
                elif object_name == 'chair'and ob_flag != 5:#已测试
                    os.system("play ~/Desktop/wrc_demo/wrc_file/chair.mp3 ")
                    print('椅子')
                    ob_flag = 5
                elif object_name == 'pottedplant'and ob_flag != 6:#已测试
                    os.system(" play ~/Desktop/wrc_demo/wrc_file/plant.mp3  ")
                    print('植物')
                    ob_flag = 6
                # elif object_name == 'bird'and ob_flag != 7:#未测试×××
                #     os.system("play ~/Desktop/wrc_demo/wrc_file/bird.mp3")
                #     print('鸟')
                #     ob_flag = 7

            # print(object_name)
            log_txt.writelines(object_name + '\n')
    log_txt.close()
                    

#物品检测：订阅movidious检测节点。
def object_search():

    rospy.init_node('wrc_objects', anonymous=False)
    rospy.Subscriber("/movidius_ncs_nodelet/detected_objects_multiple", ObjectsInBoxes, callback, queue_size=1)
    rospy.spin()

if __name__ == '__main__':
    object_search()

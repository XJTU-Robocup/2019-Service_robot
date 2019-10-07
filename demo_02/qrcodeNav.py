#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import os,sys,rospy,time
import cv2 
import pyzbar.pyzbar as pyzbar
import Image,ImageEnhance

def qrcode_rt():
    reload(sys)
    sys.setdefaultencoding('utf8')#二维码识别相关
    cap = cv2.VideoCapture(0)
    while(1):
        ret,frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        #测试代码：用来保存图片
        # cv2.imwrite('qrcode.jpg',gray)
        # image = 'qrcode.jpg'    
        # img = Image.open(image)  
          
        barcodes = pyzbar.decode(gray)
        barcodesData = 0
        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            time.sleep(2)
            if len(barcodeData) >= 1:
                return barcodeData
                break
x_flag = 0x00
def search_key():
    global x_flag
    data = qrcode_rt()
    if '餐厅' in data and x_flag != 1:
        os.system('play ~/Desktop/wrc_demo/wrc_file/ct.mp3')
        x_flag = 1
    elif '卧室' in data and  x_flag != 2:
        os.system('play ~/Desktop/wrc_demo/wrc_file/ws.mp3')
        x_flag = 2
    elif '书房' in data and x_flag != 4:
        os.system('play ~/Desktop/wrc_demo/wrc_file/sf.mp3')
        x_flag = 4
    elif '客厅' in data and x_flag != 8:
        os.system('play ~/Desktop/wrc_demo/wrc_file/kt.mp3')
        x_flag = 8
    else:
        print(data)


if __name__ ==  '__main__':
    try:
        
        while True:
            # os.system('eog qrcode.jpg')
            search_key()

    except rospy.ROSInterruptException:
        rospy.loginfo('结束')

#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import cv2
import sys,select,termios,tty

#建立地图加载
path_in = 'map.pgm'
img_in=cv2.imread(path_in)

#标准地图加载
path_s='9898.pgm'
simg_in=cv2.imread(path_s)
sgray=cv2.cvtColor(simg_in, cv2.COLOR_RGB2GRAY)
ths, s_map= cv2.threshold(sgray,50,255, cv2.THRESH_BINARY)

x0=0
y0=0

#获取鼠标点击坐标，计算分数
def getxy(event,x,y,flags,param):
        global x0,y0
        if event == cv2.EVENT_LBUTTONDOWN:
                x0=x
                y0=y
                i_map = img[ y0 : y0+98, x0 : x0+98 ]
                score(i_map,s_map)

#与标准地图进行像素对比，计算分数
def score(map_in,map_s):
        sum=0
        for y in range(0,98):
                for x in range(0,98):
                        if map_in[y,x]==255 and map_s[y,x]==255:
                                result =1
                        elif map_in[y,x]==0 and map_s[y,x]==255:
                                result =0
                        elif map_in[y,x]==255 and map_s[y,x]==0:
                                result =0
                        elif map_in[y,x]==0 and map_s[y,x]==0:
                                result =1
                        sum+=result
        # print('number',sum)
        score=int((float(sum)/9604*133.388))
        print('score',score)
        return score
cv2.namedWindow('map')
cv2.setMouseCallback('map',getxy)
d=0.0
while True:
        M=cv2.getRotationMatrix2D((0,0),d,1.0)
        img_r=cv2.warpAffine(img_in,M,(480,480))
        cv2.imshow('map',img_r)
        gray = cv2.cvtColor(img_r, cv2.COLOR_RGB2GRAY)    
        th, img = cv2.threshold(gray,220,255, cv2.THRESH_BINARY)
        i_map = img[ y0 : y0+98, x0 : x0+98 ]
        cv2.imshow('cut_map',i_map)
        # cv2.imshow('smap',s_map)        
        key=cv2.waitKey(20)
        # print key
        if key==119:
                d+=0.1
        elif key==115:
                d-=0.1

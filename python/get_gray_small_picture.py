#coding: utf-8

#从大图中提取灰度小图
#快捷键：s保存，-缩小，+放大

import cv2
import os

#--------输入参数--------
#图片源目录，不处理子目录
input_dir = 'C:\Users\Public\Pictures\Sample Pictures'

#小图尺寸
rect_width = 64
rect_height = 64

#--------全局变量--------
width,height=0,0
x_rect = 0
y_rect = 0
x_rect_drag = 0
y_rect_drag = 0
x_drag_start = -1
y_drag_start = -1
drag = 0
coefficient = 1.0
img_origin = None

def init():
    global width,height,x_rect,y_rect,x_rect_drag,y_rect_drag,x_drag_start,y_drag_start,drag,coefficient,img_origin

    width,height=0,0
    x_rect = 0
    y_rect = 0
    x_rect_drag = 0
    y_rect_drag = 0
    x_drag_start = -1
    y_drag_start = -1
    drag = 0
    coefficient = 1.0
    img_origin = None

def click_and_crop(event, x, y, flags, param):
    global width,height,x_rect,y_rect,x_rect_drag,y_rect_drag,x_drag_start,y_drag_start,drag,coefficient,img_origin

    if event == cv2.EVENT_LBUTTONDOWN:
        x_drag_start = x
        y_drag_start = y
        drag = 1

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        drag = 0
        x_drag_start = -1
        y_drag_start = -1
        x_rect = x_rect_drag
        y_rect = y_rect_drag
    elif event == cv2.EVENT_MOUSEMOVE and drag == 1:
        x_inc = x - x_drag_start
        y_inc = y - y_drag_start
        x_rect_drag = x_rect + x_inc
        y_rect_drag = y_rect + y_inc
        img = img_origin.copy()
        img = cv2.resize(img, (int(width*coefficient), int(height*coefficient)))
        cv2.rectangle(img, (x_rect_drag, y_rect_drag), (x_rect_drag + rect_width, y_rect_drag + rect_height), (0, 255, 0), 2)
        cv2.imshow("image", img)

def handle_picture(filename):
    global width,height,x_rect,y_rect,x_rect_drag,y_rect_drag,x_drag_start,y_drag_start,drag,coefficient,img_origin

    init()
    img_origin = cv2.imread(filename)
    if img_origin == None:
        return
    height, width, channels = img_origin.shape
    current_width = width
    current_height = height
    x_rect = (width - rect_width)/2
    y_rect = (height- rect_height)/2
    global img
    img = img_origin.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)

    cv2.rectangle(img, (x_rect,y_rect), (x_rect+rect_width,y_rect+rect_height), (0, 255, 0), 2)
    cv2.imshow("image", img)
    while True:
        ch = cv2.waitKey(0)
        if ch==255:
            break
        elif ch==45 or ch==95 or ch==43 or ch==61:     # -=_+4个键缩放
            if ch==43 or ch==61:     #放大
                coefficient += 0.1
            else:
                if coefficient<=0.1:
                    continue
                coefficient -= 0.1
            img = img_origin.copy()
            img = cv2.resize(img, (int(width*coefficient), int(height*coefficient)))
            coefficient_inc = (width*coefficient - current_width)/current_width #本次缩放系数增量
            x_rect = int(x_rect * (coefficient_inc + 1))
            y_rect = int(y_rect * (coefficient_inc + 1))
            current_width = int(width*coefficient)
            current_height = int(height*coefficient)
            cv2.rectangle(img, (x_rect,y_rect), (x_rect+rect_width,y_rect+rect_height), (0, 255, 0), 2)
            cv2.imshow("image", img)
        elif ch==115:   #s
            img_small = img[y_rect:y_rect+rect_height,x_rect:x_rect+rect_width]
            gray = cv2.cvtColor(img_small, cv2.COLOR_BGR2GRAY)
            if not os.path.exists('out'):
                os.mkdir('out')
            cv2.imwrite('out/'+os.path.basename(filename), gray)
            break
        else:
            print('key:', ch)

    # close all open windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    for filename in os.listdir(input_dir):
        fullfilename = os.path.join(input_dir, filename)
        if os.path.isdir(fullfilename):
            continue
        print(fullfilename)
        handle_picture(fullfilename)

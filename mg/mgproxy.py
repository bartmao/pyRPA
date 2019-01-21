from rpa import UIElement, ExecutionResult
from common import configs, trace
import json
import requests
import cv2
import numpy as np
import pyscreenshot as ImageGrab
import re
from PIL import Image, ImageDraw
import win32api
import win32con
import os.path
import time

class nativemgElment(object):
    def __init__(self, selectorkey, obj):
        self.selectorkey = selectorkey
        self.obj = obj
        try:
            imgScreen = ImageGrab.grab()
            imgScreen.save('screenshot.png')
            image = cv2.imread('screenshot.png')
            template = cv2.imread('images\\' + self.selectorkey + '.png')
            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            max_val = cv2.minMaxLoc(result)[1]
            pos = np.unravel_index(result.argmax(), result.shape)
            w1 = image.shape[1]
            h1 = image.shape[0]
            w2 = template.shape[1]
            h2 = template.shape[0]
            x1 = pos[1]
            y1 = pos[0]
            x2 = x1 + w2
            y2 = y1 + h2
            self.x = x1
            self.y = y1
            self.w = w2
            self.h = h2
            self.conf = max_val
            self.center = (int((x1+x2)/2), int((y1+y2)/2))
            trace('conf:%d on (%d,%d)(%d,%d)' % (max_val, x1, y1, x2, y2))
        finally:
            # delete screenshot
            if(os.path.isfile('screenshot.png')):
                pass

class mgElement(UIElement):
    THRES_CONFIDENCE = 0.9

    def __click(self, ele, args):
        button = args['button']
        ptype = args['type']
        clickpos = args['pos']
        
        op1 = win32con.MOUSEEVENTF_LEFTDOWN
        op2 = win32con.MOUSEEVENTF_LEFTUP
        if(button == 1):
            op1 = win32con.MOUSEEVENTF_RIGHTDOWN
            op2 = win32con.MOUSEEVENTF_RIGHTUP
        elif(button == 2):
            op1 = win32con.MOUSEEVENTF_MIDDLEDOWN
            op2 = win32con.MOUSEEVENTF_MIDDLEUP
        
        x = ele.center[0]
        y = ele.center[1]
        if(clickpos == 0):
            x = ele.x
            y = ele.y
        elif(clickpos == 1):
            x = ele.x + ele.w
            y = ele.y
        elif(clickpos == 2):
            x = ele.x
            y = ele.y + ele.h
        elif(clickpos == 3):
            x = ele.x+ele.w
            y = ele.y + ele.h
        win32api.SetCursorPos((x,y))
        
        if(ptype == 0):
            win32api.mouse_event(
                win32con.MOUSEEVENTF_LEFTDOWN,x,y, 0, 0)
            win32api.mouse_event(
                win32con.MOUSEEVENTF_LEFTUP, x,y, 0, 0)
        elif(ptype == 1):
            win32api.mouse_event(
                win32con.MOUSEEVENTF_LEFTDOWN,x,y, 0, 0)
            win32api.mouse_event(
                win32con.MOUSEEVENTF_LEFTUP, x,y, 0, 0)
            time.sleep(0.3)
            win32api.mouse_event(
                win32con.MOUSEEVENTF_LEFTDOWN,x,y, 0, 0)
            win32api.mouse_event(
                win32con.MOUSEEVENTF_LEFTUP, x,y, 0, 0)
        elif(ptype == 2):
            win32api.mouse_event(
                win32con.MOUSEEVENTF_LEFTDOWN,x,y, 0, 0)
        elif(ptype == 3):
            win32api.mouse_event(
                win32con.MOUSEEVENTF_LEFTUP, x,y, 0, 0)

    def execute(self, obj):
        if(obj['selector'].startswith('<image ')):
            # dict = {}
            # pairs = re.findall(r'\s(.+?)=[\'|"](.*?)[\'|"]', obj['selector'])
            # for p in pairs:
            #     dict[p[0]] = p[1]

            # get image element
            ele = nativemgElment(self.selectorkey, self.selector)
            if(ele.conf < mgElement.THRES_CONFIDENCE):
                return ExecutionResult(-1, message='Cannot detect this image')

            method = obj['method']
            args = obj['args']
            if(method == 'click'):
                self.__click(ele, args)
            else:
                return ExecutionResult(-1, 'Not support method: ' + method)
            return ExecutionResult()
            # draw = ImageDraw.Draw(imgScreen)
            # draw.rectangle((pos, (pos[0]+100, pos[1]+100)), fill='black')
            # imgScreen.save('screenshot.png')
            # imgScreen.show()
        return ExecutionResult(-1, message='Invalid selector ' + self.selectorkey)

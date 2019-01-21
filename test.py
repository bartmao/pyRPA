from android.droidagent import DroidAdapter, DroidElement
from rpa import InputMethod, MouseButton, Position, ClickType
import os.path
import cv2
import numpy as np
from mg.mgproxy import mgElement
from PIL import Image, ImageDraw
# template = cv2.imread('s.png')
# image = cv2.imread('l.png')
# result  = cv2.matchTemplate(image,template, cv2.TM_CCOEFF_NORMED)
# print(np.unravel_index(result.argmax(), result.shape))

if __name__ == '__main__':    
    mgElement('img_btn_windows').click(button=MouseButton.Right, type=ClickType.Doulbe)
    # image = cv2.imread('screenshot.png')
    # #template = cv2.imread('images\\img_icon_recycle.png')
    # template = cv2.imread('2.png')
    # result  = cv2.matchTemplate(image,template, cv2.TM_CCOEFF_NORMED)
    # pos = np.unravel_index(result.argmax(), result.shape)
    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # print('confidence: ' + max_val)
    # print(min_val, max_val, min_loc, max_loc)
    # w1 = image.shape[1]
    # h1 = image.shape[0]
    # w2 = template.shape[1]
    # h2 = template.shape[0]
    # x1 = pos[1]
    # y1 = pos[0]
    # x2 = x1 + w2
    # y2 = y1 + h2
    # image = Image.open('screenshot.png')
    # draw = ImageDraw.Draw(image)
    # draw.rectangle(((x1, y1), (x2, y2)), fill='black')
    # #imgScreen.save('screenshot.png')
    # image.show()
    # print(w1, h1, w2, h2)
    # print(result.shape)
    # print(pos)
    # print(x1, y1, x2, y2)

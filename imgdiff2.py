#
# 輪郭抽出サンプルプログラム
#
#   q を押すと終了する
#

import sys
import cv2
import numpy as np
from PIL import Image

MODE = 0 if len(sys.argv)!=2 else int(sys.argv[1])
# 0 : 青線輪郭のみ
# 1 : 赤線輪郭長重

file  = 'test.mp4'
win   = 'sample'
camid = 0
delay = 33

cap = cv2.VideoCapture(camid)

if not cap.isOpened():
    sys.exit()

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#fps = cap.get(cv2.CAP_PROP_FPS)
vw  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
vh  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(file, fourcc, 10, (vw, vh))
op  = np.ones((3,3), np.uint8)

while True:
    ret, frame = cap.read()

    img_gry = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_cny = cv2.Canny   (img_gry, 30, 100)
    img_dil = cv2.dilate  (img_cny, op, iterations=1)
    img_fg  = np.array(img_dil)

    img_bg = np.array(frame)
    img = img_bg.copy()

    img[:,:,0] = img_fg[:,:]
    img[:,:,1] = img_fg[:,:]
    img[:,:,2] = np.zeros((vh,vw), np.uint8)

    if MODE==1 :
      img = ~img_bg * ~img # 赤線輪郭長重モード
    else :
      img =            img # 青線輪郭のみモード

    cv2.imshow(win, img)
    out.write(img)

    c = cv2.waitKey(delay) & 0xFF
    if c == ord('q'):
        break

cap.release()
out.release()
cv2.destroyWindow(win)

quit()

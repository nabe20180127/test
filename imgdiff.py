#
# 画像差分表示サンプルプログラム
#
#   q を押すと終了する
#   c を押しても何もしない
#
#カメラで差分画像を表示する
#

import sys
import cv2
import numpy as np

window_name='follow'
camera_id   = 0
delay       = 33


def dilation(dilationSize, kernelSize, img):  # 膨張した画像にして返す
    kernel = np.ones((kernelSize, kernelSize), np.uint8)
    element = cv2.getStructuringElement(
        cv2.MORPH_RECT, 
        (2 * dilationSize + 1, 2 * dilationSize + 1),
        (dilationSize, dilationSize))
    dilation_img = cv2.dilate(img, kernel, element)
    return dilation_img

cap = cv2.VideoCapture(camera_id)
if not cap.isOpened():
    sys.exit()

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#fps    = cap.get(cv2.CAP_PROP_FPS)
vidw = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
vidh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
out = cv2.VideoWriter('test.mp4', fourcc, 30, (int(vidw), int(vidh)))

ret, frame_p  = cap.read()

while True:
    ret, frame = cap.read()
    color_diff = cv2.absdiff(frame_p , frame)
    frame_p  = frame.copy()


    gray_diff = cv2.cvtColor(color_diff, cv2.COLOR_BGR2GRAY)
    retval, black_diff = cv2.threshold(gray_diff, 45, 255, cv2.THRESH_BINARY)

    dilationSize = 2
    kernelSize   = 5
    dilation_img = dilation(dilationSize, kernelSize, black_diff) 

    image, contours, hierarchy = cv2.findContours(
        dilation_img,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE)

#    img = cv2.drawContours(frame, contours, -1, (0,255,0), 1)

    img = frame

    for i in range(len(contours)):
      count = len(contours[i])
      if count==1 :
        x0=contours[i][0][0][0]
        y0=contours[i][0][0][1]
        img = cv2.circle(frame, (x0, y0), 10, (0, 255, 255), 1)
      else :
        j=0
        while True:
          if j != (count-2) :
            x0=contours[i][j][0][0]
            y0=contours[i][j][0][1]
            x1=contours[i][j+1][0][0]
            y1=contours[i][j+1][0][1]
          else :
            x0=contours[i][count-1][0][0]
            y0=contours[i][count-1][0][1]
            x1=contours[i][0][0][0]
            y1=contours[i][0][0][1]

          img = cv2.line(frame, (x0, y0), (x1,y1), (0, 255, 0), 1)

          if j == (count-2) :
            break
          j += 1

    cv2.imshow(window_name, img)
    out.write(img)

    c = cv2.waitKey(delay) & 0xFF 

    if c == ord('c'):
        pass

    elif c == ord('q'):
        break

cap.release()
out.release()
cv2.destroyWindow(window_name)

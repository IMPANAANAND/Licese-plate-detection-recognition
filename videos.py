# -*- coding: utf-8 -*-
"""Videos.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iYmtLvWMqt4iiUlnAFKwSugjY99nVuXw
"""

from cv2 import waitKey
import torch
import cv2
import numpy as np
import time

model_path = r"/content/automatic-number-plate-recognition/best.pt"
video_path = r"/content/automatic-number-plate-recognition/anpr_video.mp4"
cpu_or_cuda = "cpu"  #choose device; "cpu" or "cuda"(if cuda is available)
device = torch.device(cpu_or_cuda)
model = torch.hub.load('ultralytics/yolov5', 'custom', path= model_path, force_reload=True)
model = model.to(device)
frame = cv2.VideoCapture(video_path)

frame_width = int(frame.get(3))
frame_height = int(frame.get(4))
size = (frame_width, frame_height)
writer = cv2.VideoWriter('output.mp4',-1,8,size)

text_font = cv2.FONT_HERSHEY_PLAIN
color= (0,0,255)
text_font_scale = 1.25
prev_frame_time = 0
new_frame_time = 0

from google.colab.patches import cv2_imshow
while True:
    ret, image = frame.read()
    if ret:
        output = model(image)
        result = np.array(output.pandas().xyxy[0])
        for i in result:
            p1 = (int(i[0]),int(i[1]))
            p2 = (int(i[2]),int(i[3]))
            text_origin = (int(i[0]),int(i[1])-5)
            #print(p1,p2)
            cv2.rectangle(image,p1,p2,color=color,thickness=2)  #drawing bounding boxes
            cv2.putText(image,text=f"{i[-1]} {i[-3]:.2f}",org=text_origin,
                        fontFace=text_font,fontScale=text_font_scale,
                        color=color,thickness=2)  #class and confidence text

        new_frame_time = time.time()

        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)
        fps = str(fps)
        cv2.putText(image, fps, (7, 70), text_font, 3, (100, 255, 0), 3, cv2.LINE_AA)
        writer.write(image)
        cv2_imshow(image)


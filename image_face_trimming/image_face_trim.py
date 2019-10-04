#------------------------------------------------------------------------------
# Image Face Triming Tool
# Copyright (c) 2019, scpepper All rights reserved.
#------------------------------------------------------------------------------

import numpy as np
import os
import sys
import cv2
import tensorflow as tf
import glob

#import os.path as osp
import numpy as np
import torch
import RRDBNet_arch as arch


model_file = "./models/human_face_detection.pb"

# Input Definition
detection_graph = tf.Graph()
with detection_graph.as_default():
    with open(model_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name="")
sess = tf.Session(graph=detection_graph)

color=(255, 255, 0)
height,width = 64,64

def draw_box(img, box, color, score):
    x, y, w, h = box
    label = 'face '+str(int(score*100))+'%'  #self.name
    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
    label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1.5, 1)
    cv2.rectangle(img, (x, y), (x + label_size[0], y + label_size[1] + base_line), color, cv2.FILLED)
    cv2.putText(img, label, (x, y + label_size[1]), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0))

def main(argv):

    image_in = argv[1]
    image_out = argv[2]

    files = glob.glob(image_in + "/*.jpg")
    for file in files:

        image_file = file
        print(image_file)

        x, y, w, h = 0, 0, 0, 0

        image_np = cv2.imread(image_file)
    #    image_np = cv2.resize(frame,(cam_width,cam_height))
        image_np_expanded = np.expand_dims(image_np, axis=0)
        print(image_np.shape[1])
        cam_height = image_np.shape[0]
        cam_width = image_np.shape[1]

        # Input Definition
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        scores = detection_graph.get_tensor_by_name('detection_scores:0')
        classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')

        # Actual detection.
        (boxes, scores, classes, num_detections) = sess.run(
            [boxes, scores, classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})

        # Visualize Objects
        num_persons=0
        for i in range(boxes[0].shape[0]):
            if scores[0][i] >= 0.5:
                num_persons+=1

                im_height, im_width, _ = image_np.shape
                ymin, xmin, ymax, xmax = tuple(boxes[0][i].tolist())
                (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                            ymin * im_height, ymax * im_height)

                x, y, w, h = int(left), int(top), int(right - left), int(bottom - top)
    #                draw_box(image_np, (x, y, w, h), color, scores[0][i])

    #        cv2.putText(image_np, "There are " + str(num_persons) + " persons.", (0, 100), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 5, cv2.LINE_AA)
    #        cv2.imshow("camera window", image_np)

                if x > 0 and y > 0 and w > 0 and h > 0 :
            #        print(h,y,w,x)
            #            image_trm = image_np[y : y + h, x : x + w]
                    y_top = int(y - (h/3))
                    y_bottom = int(y + h + (h/3))
                    x_left = int(x - (w/3))
                    x_right = int(x + w + (w/3))
                    print(int(y_top), int(y_bottom), int(x_left), int(x_right))
                    if y_top < 0:
                        y_top = 0
                    if y_bottom > cam_height:
                        y_bottom = cam_height
                    if x_left < 0:
                        x_left = 0
                    if x_right > cam_width:
                        x_right = cam_width
            
                    image_trm = image_np[y_top : y_bottom, x_left : x_right]

                    image_trm_resize = cv2.resize(image_trm, dsize=(150,200))

                    cv2.imwrite(image_out+"/trimed_"+str(i)+"_"+os.path.basename(file),image_trm_resize)

if __name__ == '__main__':
    main(sys.argv)


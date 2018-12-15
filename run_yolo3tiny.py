
from PIL import Image
import numpy as np

import sys
sys.path.append('./keras-yolo3')
from yolo import YOLO

def detect_img(yolo):
    while True:
        img = input('Input image filename:')
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            r_image = yolo.detect_image(image)
            print(type(r_image))
            import cv2
            cv2.imwrite("out.jpg", np.asarray(r_image)[..., ::-1])
            r_image.show()
    yolo.close_session()

if __name__ == '__main__':
    model_path = 'keras-yolo3/model_data/yolo-tiny.h5'
    anchors_path = 'keras-yolo3/model_data/tiny_yolo_anchors.txt'
    classes_path = 'keras-yolo3/model_data/coco_classes.txt'
    model = YOLO(model_path=model_path, anchors_path=anchors_path, classes_path=classes_path)
    detect_img(model)

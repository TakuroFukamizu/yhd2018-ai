import coremltools
import sys
sys.path.append('./keras-yolo3')
from yolo import YOLO

if __name__ == '__main__':
    model_path = 'keras-yolo3/model_data/yolo-tiny.h5'
    anchors_path = 'keras-yolo3/model_data/tiny_yolo_anchors.txt'
    classes_path = 'keras-yolo3/model_data/coco_classes.txt'
    model = YOLO(model_path=model_path, anchors_path=anchors_path, classes_path=classes_path)

    keras_model = model.yolo_model
    keras_model.summary()

    is_bgr = False
    
    mlmodel = coremltools.converters.keras.convert(
        keras_model,
        image_input_names='input_1'
        )
    spec = mlmodel.get_spec()
    print(spec.description)
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app, flags, logging
from absl.flags import FLAGS
import core.utils as utils
from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
from PIL import Image
import cv2
import json, pathlib
from easydict import EasyDict
import numpy as np
import random
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

flags.DEFINE_string('framework', 'tf', '(tf, tflite, trt')
# weights 설정
flags.DEFINE_string('weights', './checkpoints/v4_weight',
                    'path to weights file')
# size 설정
flags.DEFINE_integer('size', 416, 'resize images to') # define_img_size
flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny') # used tiny_version or original_version
flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4') # choose model
# 이미지 경로 설정
flags.DEFINE_string('image', 'data/kite.jpg', 'path to input image')
# iou 수치 설정
flags.DEFINE_float('iou', 0.45, 'iou threshold')
# loss 수치 설정
flags.DEFINE_float('score', 0.25, 'score threshold')

def main(_argv):
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(FLAGS)
    input_size = FLAGS.size
    image_path = FLAGS.image
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    image_data = cv2.resize(original_image, (input_size, input_size))
    image_data = image_data / 255.

    images_data = []
    for i in range(1):
        images_data.append(image_data)
    images_data = np.asarray(images_data).astype(np.float32)

    if FLAGS.framework == 'tflite':
        interpreter = tf.lite.Interpreter(model_path=FLAGS.weights)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        interpreter.set_tensor(input_details[0]['index'], images_data)
        interpreter.invoke()
        pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
        if FLAGS.model == 'yolov3' and FLAGS.tiny == True:
            boxes, pred_conf = filter_boxes(pred[1], pred[0], score_threshold=0.25, input_shape=tf.constant([input_size, input_size]))
        else:
            boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25, input_shape=tf.constant([input_size, input_size]))

    else:
    # called weights from line of 19
        saved_model_loaded = tf.saved_model.load(FLAGS.weights, tags=[tag_constants.SERVING])
        infer = saved_model_loaded.signatures['serving_default']
        batch_data = tf.constant(images_data)
        pred_bbox = infer(batch_data)
        for key, value in pred_bbox.items():
            boxes = value[:, :, 0:4]
            pred_conf = value[:, :, 4:]

    boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        scores=tf.reshape(
            pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        max_output_size_per_class=50,
        max_total_size=50,
        iou_threshold=FLAGS.iou,
        score_threshold=FLAGS.score
    )
    pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]

    # image = utils.draw_bbox(original_image, pred_bbox)
    # image = Image.fromarray(image.astype(np.uint8))
    # image.show()
    # image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    # cv2.imwrite(FLAGS.output, image)

    # price_dict = {}
    # for i in range(41):
    #     if i == 0:
    #         price = i + random.randint(1000, 100000)
    #         price_dict[i] = price
    #     else:
    #         price = i * random.randint(1000, 10000)
    #         price_dict[i] = price
    json_data = EasyDict()
    class_json = utils.pass_on_bbox(original_image, pred_bbox)

    if len(class_json) == 0:
        print('Not Detecting')
    else:
        json_data['IMG'] = {'file_name': image_path.split('\\')[-1], 'file_size': (Image.open(image_path)).size}
    # if class_json['price'] in price_dict.keys():
    #     class_json['price'] = "{:,}원".format(price_dict[class_json['price']])

    json_data['annotation'] = class_json
    json_file = json.dumps(str(json_data), ensure_ascii=False, indent=2)

    print(json_file)
    return json_file


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass

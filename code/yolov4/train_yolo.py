from tensorflow.keras import callbacks
from yolov4.tf import YOLOv4, YOLODataset, SaveWeightsCallback

yolo = YOLOv4()

# class name
yolo.config.parse_names("marvel.names")
# Context-Free Grammar
yolo.config.parse_cfg("yolov4-tiny.cfg")

yolo.make_model()
# load pre_trained weights
yolo.load_weights(
    "yolov4-tiny.weights",
    weights_type="yolo",
)
yolo.summary(summary_type="yolo")

for i in range(29):
    yolo.model.get_layer(index=i).trainable = False

yolo.summary()

# Train_set
# image class,x,y,w,h class,x,y,w,h class,x,y,w,h ....
train_dataset = YOLODataset(
    config=yolo.config,
    dataset_list="D:/marvel_train.txt",
    # If you want to directory,
    # image_path_prefix="/content/train2017",
    training=True,
)

# Val_set
val_dataset = YOLODataset(
    config=yolo.config,
    dataset_list="D:/marvel_val.txt",
    # image_path_prefix="/content/val2017",
    training=False,
)

yolo.compile()

_callbacks = [
    callbacks.TerminateOnNaN(),
    callbacks.TensorBoard(
        # Directory for tensorBoard
        log_dir="marvel/",
        update_freq=200,
        histogram_freq=1,
    ),
    SaveWeightsCallback(
        yolo=yolo,
        dir_path="marvel/",
        weights_type="yolo",
        step_per_save=2000,
    ),
]

yolo.fit(
    train_dataset,
    callbacks=_callbacks,
    validation_data=val_dataset,
    verbose=3  # 3: print step info
)

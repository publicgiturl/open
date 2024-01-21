
import json
from onss import ConvertEncoder
import cv2
import tensorflow as tf
from tqdm import tqdm
record_iterator = tf.compat.v1.python_io.tf_record_iterator(
	path='/data/data/car_plate/drive-download-20230404T064518Z-001/train.tfrecord')

# iterate through each record in the file
for string_record in tqdm(record_iterator):
	# parse the example from the record
	example = tf.train.Example()
	example.ParseFromString(string_record)

	# get the image data and label
	image_string = example.features.feature['image/encoded'].bytes_list.value[0]
	file_name = str(example.features.feature['image/filename'].bytes_list.value[0]).split("'")[1]
	json_name = file_name.split('.')[0]+'.json'


	ymin = example.features.feature['image/object/bbox/ymin'].float_list.value[0]
	ymax = example.features.feature['image/object/bbox/ymax'].float_list.value[0]
	xmin = example.features.feature['image/object/bbox/xmin'].float_list.value[0]
	xmax = example.features.feature['image/object/bbox/xmax'].float_list.value[0]
	label = str(example.features.feature['image/object/class/text'].bytes_list.value[0]).split("'")[1]
	# convert the image string to a numpy array
	image = tf.image.decode_jpeg(image_string).numpy()
	json_data = dict(
		label = label,
		bbox = [xmin, ymin, xmax, ymax],
		file_name = file_name
	)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	with open(f'/data/data/sample/labels/{json_name}', 'w', encoding='utf-8') as json_file:
		json.dump(json_data, json_file, ensure_ascii=False, indent=2, cls=ConvertEncoder)
	cv2.imwrite(f'/data/data/sample/images/{file_name}', image)

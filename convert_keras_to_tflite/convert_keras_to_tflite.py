import os, sys
import tensorflow as tf

in_file = sys.argv[1]
print(in_file)

file_id, file_ext = os.path.splitext(in_file)

converter = tf.lite.TFLiteConverter.from_keras_model_file(in_file)
tflite_model = converter.convert()
open(file_id + ".tflite", "wb").write(tflite_model)

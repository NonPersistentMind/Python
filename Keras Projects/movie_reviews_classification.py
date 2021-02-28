import tensorflow as tf
from tensorflow.python.keras.backend import set_session
config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.3
config.gpu_options.visible_device_list = "0"
set_session(tf.compat.v1.Session(config=config))


from keras.datasets import imdb
from keras.utils import to_categorical
from keras import models, layers, optimizers, losses, metrics
import numpy as np
# =========================== Function initialization ============================

MAX_WORD_NUM = 10000

num_to_word = {value:key for (key,value) in imdb.get_word_index().items()}

def decode_review(encoded_review):
  arr = [num_to_word.get(num-3, 'UNKNOWN') for num in encoded_review]
  return ' '.join(arr)


def vectorize_sequences(sequences):
  result = np.zeros((len(sequences), MAX_WORD_NUM))
  for i, sequence in enumerate(sequences):
    result[i,sequence] = 1
  return result


def build_model(input_shape, activation_name='relu', shape=(16,16), dropout=False):
  network = models.Sequential()

  network.add(layers.Dense(shape[0], activation=activation_name, input_shape=input_shape))

  for layer_size in shape[1:]:
    network.add(layers.Dense(layer_size, activation=activation_name))

  network.add(layers.Dense(1, activation='sigmoid'))

  network.compile(optimizer=optimizers.RMSprop(), loss=losses.binary_crossentropy, metrics=[metrics.binary_accuracy])

  return network


# =============================== Data Preparation ===============================

(train_samples, train_labels),  (test_samples,test_labels) = imdb.load_data(num_words=MAX_WORD_NUM)

train_samples = vectorize_sequences(train_samples)
test_samples = vectorize_sequences(test_samples)

train_labels = np.asarray(train_labels, dtype='float32')
test_labels = np.asarray(test_labels, dtype='float32')

EXCHANGE_PART = 15000
VALIDATION_PART=7500

train_samples = np.concatenate((train_samples, test_samples[:EXCHANGE_PART]))
test_samples = test_samples[EXCHANGE_PART:]

train_labels = np.concatenate((train_labels, test_labels[:EXCHANGE_PART]))
test_labels = test_labels[EXCHANGE_PART:]


# ============================= Building the Network =============================

shapes = [ 
          (4,4)
          , (4,4,4), (16,16)
          # ,  (16,16,16), (32,32), (32,32,32)
          # (32,16,32), (64,64), (64,64,64), (64,16,64), (64,32,64), (128,128)
          ]
validation_histories = []
EPOCHS = 10

for shape in shapes:
  # shape=shapes[]
  model = build_model(train_samples[0].shape, shape=shape)
  history = model.fit(train_samples, train_labels, batch_size=32, epochs=EPOCHS, validation_split=0.15, verbose=False)

  validation_histories.append(history.history['val_loss'])

print(validation_histories)

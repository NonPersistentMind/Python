import keras
from keras import callbacks
from keras.utils import to_categorical
from keras import layers, models, metrics, losses, optimizers
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from data_extraction import data_folders, data_location
import os
plt.style.use('ggplot')

BATCH_SIZE = 50
EPOCHS = 100

PROJECT_DIR = '/home/andrew_lick/Desktop/Books_lib/Keras Projects/Cats&Dogs'
# ============================= Data Preprocesssing ==============================

train_datagen = ImageDataGenerator(
    rescale=1/255, rotation_range=60, width_shift_range=0.2,
    height_shift_range=0.2, shear_range=0.2, zoom_range=0.2,
    fill_mode='nearest')
val_datagen = ImageDataGenerator(rescale=1/255)

train_generator = train_datagen.flow_from_directory(
    data_folders['train'], target_size=(150, 150), batch_size=BATCH_SIZE, class_mode='binary')
validation_generator = val_datagen.flow_from_directory(
    data_folders['validation'], target_size=(150, 150), batch_size=BATCH_SIZE, class_mode='binary')

# for data_batch, label_batch in train_generator:
#     print(label_batch)
#     break


# ============================== Building The Model ==============================

network = models.Sequential()
network.add(layers.Conv2D(
    64, (3, 3), activation='relu', input_shape=(150, 150, 3)))
network.add(layers.MaxPooling2D(pool_size=(2, 2)))
network.add(layers.Conv2D(64, (3, 3), activation='relu'))
network.add(layers.MaxPooling2D(pool_size=(2, 2)))
network.add(layers.Conv2D(128, (3, 3), activation='relu'))
network.add(layers.MaxPooling2D(pool_size=(2, 2)))
network.add(layers.Conv2D(128, (3, 3), activation='relu'))
network.add(layers.MaxPooling2D(pool_size=(2, 2)))
network.add(layers.Flatten())
network.add(layers.Dropout(0.5))
network.add(layers.Dense(512, activation='relu'))
network.add(layers.Dense(1, activation='sigmoid'))


# ============================== Create Checkpoints ==============================
checkpoint_dir = os.path.join(PROJECT_DIR, 'Pretrained_Model')
callbacks = [keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_dir+'/ckp_25.02', save_best_only=True, monitor='val_binary_accuracy', mode='max')]


# print(network.summary())
network.compile(optimizer=optimizers.RMSprop(),
                loss=losses.binary_crossentropy, metrics=[metrics.binary_accuracy])

history = network.fit(train_generator, steps_per_epoch=2000/BATCH_SIZE, epochs=EPOCHS,
                      validation_data=validation_generator, validation_steps=1000/BATCH_SIZE, callbacks=callbacks)

network.save('cats-dogs_v2_dropout_100epochs.h5')


# ======================= Plotting The Network Performance =======================
epochs = range(1, EPOCHS+1)

plt.figure(figsize=(15, 7), dpi=100).suptitle('Network Performance')

plt.subplot(1, 2, 1)
plt.plot(epochs, history.history['binary_accuracy'], label='Accuracy')
plt.plot(epochs, history.history['val_binary_accuracy'], label='Val Accuracy')
plt.legend(loc='lower right')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs, history.history['loss'], label='Loss')
plt.plot(epochs, history.history['val_loss'], label='Val Loss')
plt.legend(loc='upper left')
plt.xlabel('Epochs')
plt.ylabel('Loss')

plt.show()

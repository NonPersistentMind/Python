import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from keras.applications import VGG16 as VGG
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models, optimizers, losses, metrics
from tensorflow.python.ops.gen_nn_ops import DataFormatDimMap
from data_extraction import data_folders
from keras.preprocessing.image import ImageDataGenerator
plt.style.use('ggplot')

# ====================== Firstly, Choose A Mode To Proceed =======================
modes = ['pure_extraction', 'augmented_extraction', 'fine_tuning']
CURRENT_MODE = modes[1]


# ================================ Define A Model ================================

train_datagen = ImageDataGenerator(rescale=1/255) if CURRENT_MODE == modes[0] else ImageDataGenerator(rescale=1/255, rotation_range=50, width_shift_range=0.3,
                                                                                                      height_shift_range=0.3, shear_range=0.3,
                                                                                                      zoom_range=0.3, horizontal_flip=True, fill_mode='nearest')
test_datagen = ImageDataGenerator(rescale=1/255)


batch_size = 20
EPOCHS = 20

conv_base = VGG(weights="imagenet", include_top=False,
                  input_shape=(150, 150, 3))


def extract_features(directory, sample_size):
    features = np.zeros(shape=(sample_size, 4, 4, 512))
    labels = np.zeros(shape=(sample_size,))
    generator = train_datagen.flow_from_directory(directory=directory,
                                                  target_size=(150, 150),
                                                  batch_size=batch_size,
                                                  class_mode='binary')

    for i, (image_batch, label_batch) in enumerate(generator):
        if i*batch_size >= sample_size:
            break
        features_batch = conv_base.predict(image_batch)
        features[i*batch_size: (i+1)*batch_size] = features_batch
        labels[i*batch_size: (i+1)*batch_size] = label_batch

    return features, labels


if 'extraction' in CURRENT_MODE:

    # ================ Only Feature Extraction, Followed By Learning =================
    if CURRENT_MODE == modes[0]:
        train_features, train_labels = extract_features(
            data_folders['train'], 2000)
        validation_features, validation_labels = extract_features(
            data_folders['validation'], 1000)
        test_features, test_labels = extract_features(
            data_folders['test'], 1000)

        train_features = train_features.reshape((len(train_features), 4*4*512))
        validation_features = validation_features.reshape(
            (len(validation_features), 4*4*512))
        test_features = test_features.reshape((len(test_features), 4*4*512))

        network = models.Sequential()
        network.add(layers.Dense(512,
                                 activation='relu',
                                 input_shape=(4*4*512,)))
        network.add(layers.Dropout(0.5))
        network.add(layers.Dense(1, activation='sigmoid'))

        network.compile(optimizer=optimizers.RMSprop(),
                        loss=losses.binary_crossentropy,
                        metrics=['accuracy'])

        history = network.fit(train_features, train_labels, batch_size=batch_size,
                              epochs=EPOCHS, validation_data=(validation_features, validation_labels))


    # ================== Feature Extraction With Data Augmentation ===================
    else:
        train_generator = train_datagen.flow_from_directory(data_folders['train'], target_size=(150,150), class_mode='binary', batch_size=batch_size)
        validation_generator = test_datagen.flow_from_directory(data_folders['validation'], target_size=(150,150), class_mode='binary', batch_size=batch_size)

        conv_base.trainable = False
        network = models.Sequential()
        network.add(conv_base)
        network.add(layers.Flatten())
        network.add(layers.Dense(256, activation='relu'))
        # network.add(layers.Dropout(0.4))
        network.add(layers.Dense(1, activation='sigmoid'))

        network.compile(optimizer=optimizers.RMSprop(lr=5e-4),
                        loss=losses.binary_crossentropy,
                        metrics=['accuracy'])

        network.fit(train_generator, batch_size=batch_size,
                              epochs=EPOCHS, validation_data=validation_generator, steps_per_epoch=100, validation_steps=50)

        

        # network.compile(optimizer=optimizers.RMSprop(lr=2e-5),
        #                 loss=losses.binary_crossentropy,
        #                 metrics=['accuracy'])

        # network.fit(train_generator, batch_size=batch_size,
        #                       epochs=EPOCHS, validation_data=validation_generator, steps_per_epoch=100, validation_steps=50)

        # ============================= Complete Fine-Tuning =============================
        trainable = False
        for layer in conv_base.layers:
            if layer.name == 'block5_conv1':
                trainable = True
            layer.trainable = trainable
        
        network.compile(optimizer=optimizers.RMSprop(lr=2e-5), loss=losses.binary_crossentropy, metrics=['accuracy'])

        history = network.fit(train_generator, epochs=EPOCHS, steps_per_epoch=100, validation_data=validation_generator, validation_steps=50)




# ========================= Plotting Network Performance =========================

epochs = range(1, EPOCHS+1)

plt.figure(figsize=(15, 7), dpi=100).suptitle('Network Performance')
plt.subplot(1, 2, 1)
plt.plot(epochs, history.history['accuracy'], label='Accuracy')
plt.plot(epochs, history.history['val_accuracy'], label='Val Accuracy')
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

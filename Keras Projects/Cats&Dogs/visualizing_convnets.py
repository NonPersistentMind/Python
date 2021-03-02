import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import matplotlib.pyplot as plt
import numpy as np
from keras.preprocessing import image
from keras import models, metrics, losses, optimizers
# plt.style.use('ggplot')

network = models.load_model(
    './Pretrained_Model/cats-dogs_v2_dropout_100epochs.h5')
# [print(layer.output) for layer in network.layers[:8]]
model = models.Model(inputs=network.input, outputs=[
                     layer.output for layer in network.layers[:8]])

img = image.load_img('./Datasets/test/cats/cat.1502.jpg',
                     target_size=(150, 150))
img_arr = image.img_to_array(img)
# print(img_arr.shape)
img_arr /= 255
img_arr = np.expand_dims(img_arr, axis=0)

activations = model.predict(img_arr)

# print(activations[0].shape)
# print(activations[0][0,:,:,6])
# # imm[:30, :30, :] = 0
# # imm[:30, :30, 0] = 1
# plt.matshow(imm, cmap='viridis')
# plt.show()

for activation_output in activations:
    activation = activation_output[0]
    plt.figure()

    columns = 16
    filters_count = activation.shape[-1]
    image_size = activation.shape[0]
    rows = filters_count // columns
    if rows*columns < filters_count:
        rows += 1

    figure = np.zeros(shape=(image_size*rows, image_size*columns))
    for i in range(rows):
        for j in range(columns):
            rows_start, rows_end = image_size*i, image_size*(i+1)
            columns_start, columns_end = image_size*j, image_size*(j+1)
            figure[ rows_start:rows_end, columns_start:columns_end] = activation[:,:, i*columns + j]

    plt.imshow(figure)
    

plt.show()


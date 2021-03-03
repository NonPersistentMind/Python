import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from keras import models
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
tf.compat.v1.disable_eager_execution()


# Visualizing procedures:
# "Intermediate Learnings"
# "Closest Filters' Activation"
# "Heatmaps"

def normalize_image(image_arr):
    new_image = np.copy(image_arr)

    new_image -= np.mean(new_image)
    new_image /= np.std(new_image, ddof=1) + 0.5
    new_image = np.clip(new_image, 0, 1)

    return new_image*255

def step(iteration, ):
    if iteration < 15: return 1
    elif iteration < 25: return 0.2
    elif iteration < 35: return 2e-2
    else: return 5e-4


# ========================== Choosing Current Procedure ==========================

PROCEDURE = "Closest Filters' Activation"

# ==============================================================================


network = models.load_model(
    './Pretrained_Model/cats-dogs_v2_dropout_100epochs.h5')


if PROCEDURE == "Intermediate Learnings":
    model = models.Model(inputs=network.input, outputs=[
        layer.output for layer in network.layers[:8]])

    img = image.load_img('./Datasets/test/cats/cat.1502.jpg',
                         target_size=(150, 150))
    img_arr = image.img_to_array(img)
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
                figure[rows_start:rows_end,
                       columns_start:columns_end] = activation[:, :, i*columns + j]

        plt.imshow(figure)

    plt.show()

elif PROCEDURE == "Closest Filters' Activation":

    # ========================== Procedure-Specific imports ==========================
    from keras.applications import VGG16 as VGG
    from keras import backend as K
    # ==============================================================================

    # network = VGG(True, 'imagenet')
    network = models.load_model('Pretrained_Model/cats-dogs_v2_nodropout.h5')


# 'block' in layer.name and 
    layers_to_extract = [layer for layer in network.layers if ( 'conv' in layer.name)]
    
    for layer in layers_to_extract:
        layer_output = layer.output

        fig = plt.figure(layer.name, figsize=(1700,1000))
        plt.axis(False)

        columns = 16
        displayed_filters = 64
        rows = displayed_filters//columns
        margin = 5
        image_size = 150

        result = np.zeros(shape=(rows*image_size + (rows-1)*margin,
                                 columns*image_size + (columns-1)*margin, 3), dtype=np.uint8)

        for i in range(64):

            loss = K.mean(layer_output[:, :, :, i])

            grad = K.gradients(loss, network.input)[0]
            grad /= K.sqrt(K.mean(K.square(grad))) + 1e-5

            iterate = K.function(inputs=[network.input], outputs=[loss, grad])

            # loss_value, grad_value = iterate( [np.zeros(shape=(1, image_size, image_size, 3))] )

            image = np.random.random((1,image_size,image_size,3))*20 + 128

            for j in range(40):
                _, gradient_value = iterate([image])

                image += gradient_value*step(j)

            formatted_image = np.clip(normalize_image(image), 0, 255).astype('uint8')
            # print(np.min(formatted_image), np.max(formatted_image))
            # raise Exception()
            
            col_start = i%columns * image_size + max(i%columns-1, 0)*margin
            col_end = col_start + image_size
            row_start = i//columns * image_size + max(i//columns-1, 0)*margin
            row_end = row_start + image_size

            result[row_start:row_end, col_start:col_end, :] = formatted_image

            print(f'{i}-th step processed')

        plt.imshow(result)

        plt.show()

elif PROCEDURE == "Heatmaps":
    pass







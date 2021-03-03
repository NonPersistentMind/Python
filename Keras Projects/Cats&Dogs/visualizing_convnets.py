import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from keras import models
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
tf.compat.v1.disable_eager_execution()


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

# Visualizing procedures:
# "Intermediate Learnings"
# "Closest Filters' Activation"
# "Heatmaps"

PROCEDURE = "Heatmaps"

# ================================================================================


network = models.load_model(
    './Pretrained_Model/cats-dogs_v2_dropout_100epochs.h5')

# ================= Look at the activation intensity of different ================
# ======================== layers, using a specific image ========================
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


# =========================== Look at different images ===========================
# =============== that excite filters in different layers the most ===============

elif PROCEDURE == "Closest Filters' Activation":
    # ========================== Procedure-Specific imports ==========================
    from keras.applications import VGG16 as VGG
    from keras import backend as K
    # ================================================================================

    # network = VGG(True, 'imagenet')
    network = models.load_model('Pretrained_Model/cats-dogs_v2_nodropout.h5')


#   'block' in layer.name and 
    layers_to_extract = [layer for layer in network.layers if ( 'conv' in layer.name)]
    
    for layer in layers_to_extract:
        layer_output = layer.output

        fig = plt.figure(layer.name, figsize=(1700,1000))
        plt.axis(False)

        columns = 16
        displayed_filters = 64  # a power of 2, to avoid adding 1 to rows
        rows = displayed_filters//columns + (0 if (displayed_filters%columns == 0) else 1)
        margin = 5
        image_size = 150

        result = np.zeros(shape=(rows*image_size + (rows-1)*margin,
                                 columns*image_size + (columns-1)*margin, 3), dtype=np.uint8)

        for i in range(64):

            loss = K.mean(layer_output[:, :, :, i])

            grad = K.gradients(loss, network.input)[0]
            grad /= K.sqrt(K.mean(K.square(grad))) + 1e-5

            iterate = K.function(inputs=[network.input], outputs=[loss, grad])

            image = np.random.random((1, image_size, image_size, 3))*20 + 128

            for j in range(40):
                _, gradient_value = iterate([image])

                image += gradient_value*step(j)

            formatted_image = np.clip(normalize_image(image), 0, 255).astype('uint8')
            # print(np.min(formatted_image), np.max(formatted_image))
            # raise Exception()

            col_start = i % columns * image_size + max(i % columns-1, 0)*margin
            col_end = col_start + image_size
            row_start = i//columns * image_size + max(i//columns-1, 0)*margin
            row_end = row_start + image_size

            result[row_start:row_end, col_start:col_end, :] = formatted_image

            print(f'{i}-th step processed')

        plt.imshow(result)

        plt.show()


# ============== Superimpose layer's weighted activation intensity ===============
# ============ Over a real image. It helps to determine, which pixels ============
# ========= are the most responsible for specific network's predictions ==========

elif PROCEDURE == "Heatmaps":
    # ========================== Procedure-Specific imports ==========================
    from keras.applications import VGG16 as VGG
    from keras import backend as K
    import cv2
    from keras.preprocessing import image
    from keras.applications.vgg16 import preprocess_input, decode_predictions
    # ================================================================================

    network = VGG(include_top=True, weights='imagenet')
    
    img_path = 'Datasets/test/dogs/dog.1515.jpg'
    img = image.load_img(img_path, target_size=(224,224))

    img_arr = image.img_to_array(img)
    img_arr = np.expand_dims(img_arr, axis=0)
    img_arr = preprocess_input(img_arr)

    predictions = network.predict(img_arr)

    # print( np.argmax(predictions) )   # -------> Returns 253 for the image in string
    # print( decode_predictions(predictions)[0] )   # -------> Has 0.86 confidence in German Shepherd

    last_layer_output = network.get_layer('block5_conv3').output
    german_sherperd_output = network.output[:,235]

    grads = K.gradients(german_sherperd_output, last_layer_output)[0]
    # print(grads.shape)    # -------> Has (None, 14, 14, 512) shape

    pooled_grads = K.mean(grads, axis=(1,2,3))  # A vector of average filters' impact on predicting thing in K.gradients( HERE, ... )
    # Returns a filter-wise mean. That is, a vector of size 512, containig means on every available filter

    iterate = K.function(inputs=[network.input], outputs=[pooled_grads, last_layer_output[0]])

    computed_grads, computed_conv_output = iterate([img_arr])
    for i in range(len(computed_grads)):
        computed_conv_output[:, :, i] *= computed_grads[i]

    heatmap = K.mean(tf.convert_to_tensor( computed_conv_output ), axis=-1)
    # print(K.get_value(heatmap))

    heatmap = np.maximum(K.get_value(heatmap), 0)
    heatmap /= np.max(heatmap)

    plt.matshow(heatmap, cmap='plasma')
    # plt.show()


    # ====================== Superimposing Heatmap Over Picture ======================

    img = cv2.imread(img_path)
    # print(type(img))  # -------> np.ndarray

    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255*heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    intensity = 0.4
    superimposed_img = np.uint8(np.clip(img + intensity*heatmap, 0, 255))

    cv2.imwrite('picture.png', img)
    cv2.imwrite('superimposed_picture.png', superimposed_img)



    








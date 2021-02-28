from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt
from data_extraction import data_folders
import os
# plt.style.use('ggplot')
joinpath = os.path.join

path = joinpath(data_folders['train'], 'cats')
imgname = os.listdir(path)[4]

datagen = ImageDataGenerator(rescale=1/255, rotation_range=40, width_shift_range=0.2,
                             height_shift_range=0.2, shear_range=0.2, 
                             zoom_range=0.2, horizontal_flip=True, fill_mode='nearest')

img = image.load_img(joinpath(path, imgname), target_size=(150, 150))
# print(img)
img_array = image.img_to_array(img)
img_array = np.reshape(img_array, (1,) + img_array.shape)

plt.figure()
for i, batch in enumerate(datagen.flow(img_array, batch_size=1)):
    plt.subplot(3,3,i+1)
    plt.imshow(batch[0])
    if i == 8: 
        break

# # plt.imshow(img_array)
plt.show()

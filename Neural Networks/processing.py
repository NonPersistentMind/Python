import numpy as np
from matplotlib import pyplot as plt

file_data = open('train-images.idx3-ubyte', 'rb')
file_labels = open('train-labels.idx1-ubyte', 'rb')
read = file_data.read


def bytes_to_int(bytes_num):
    return int.from_bytes(read(bytes_num), byteorder='big')


# Remove magic number
magic_num = bytes_to_int(4)


# Get Dimensions
entries_count = bytes_to_int(4)
dim1 = bytes_to_int(4)
dim2 = bytes_to_int(4)

images = np.ndarray((entries_count, dim1, dim2))
for num in range(entries_count):
    image = np.zeros((dim1,dim2))
    for i in range(dim1):
        for j in range(dim2):
            image[i,j] = bytes_to_int(1)
        
    images[num] = image



# =========================== To Display an Image ==========================
# new_image = [[[(255-val)/255]*3 for val in row] for row in images[1]]
# plt.imshow(new_image, interpolation='nearest')
# plt.show()

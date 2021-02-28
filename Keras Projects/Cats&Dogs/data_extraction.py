import os, shutil
from zipfile import ZipFile

joinpath = os.path.join
# ======================= Unzip the file and move the data =======================

# test_zip_location = os.path.join(data_location, 'test1.zip')
# train_zip_location = os.path.join(data_location, 'train.zip')

# train_file = ZipFile(train_zip_location, mode='r' )
# test_file = ZipFile(test_zip_location, mode='r')

# for operation in data_operations:
#     os.mkdir( os.path.join(data_location, operation) )

# train_file.extractall(os.path.join(data_location, 'train_data'))
# test_file.extractall(os.path.join(data_location, 'test_data'))


# ==================== Move the data to corresponding folders ====================

data_location = '/home/andrew_lick/Desktop/Books_lib/Keras Projects/Cats&Dogs/Datasets'
data_operations = ['train', 'validation', 'test']
labels = ['cat', 'dog']
data_sources = {
    'train':os.path.join(data_location, 'train_data'), 
    'test':os.path.join(data_location, 'test_data')
    }
data_folders = {operation:os.path.join(data_location, operation) for operation in data_operations}

if __name__ == '__main__':
    for label in labels:
        
        # Copy training images
        filenames = [f'{label}.{i}.jpg' for i in range(1000)]
        path = joinpath(data_folders['train'], label+'s')
        os.mkdir( path )
        for filename in filenames:
            src = joinpath(data_sources['train'], filename)
            dest = joinpath(path, filename)
            shutil.copyfile(src, dest)

        # Copy validation images
        filenames = [f'{label}.{i}.jpg' for i in range(1000,1500)]
        path = joinpath(data_folders['validation'], label+'s')
        os.mkdir( path )
        for filename in filenames:
            src = joinpath(data_sources['train'], filename)
            dest = joinpath(path, filename)
            shutil.copyfile(src,dest)

        # Copy testing images
        filenames = [f'{label}.{i}.jpg' for i in range(1500,2000)]
        path = joinpath(data_folders['test'], label+'s')
        os.mkdir( path )
        for filename in filenames:
            src = joinpath(data_sources['train'], filename)
            dest = joinpath(path, filename)
            shutil.copyfile(src,dest)


        


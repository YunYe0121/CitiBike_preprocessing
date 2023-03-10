import numpy as np

def data_min_max_checker():

    training_vdata = np.load('npy_files/training_vdata.npy')
    testing_vdata = np.load('npy_files/testing_vdata.npy')
    training_fdata = np.load('npy_files/training_fdata.npy')
    testing_fdata = np.load('npy_files/testing_fdata.npy')

    print('training_vdata.max():', training_vdata.max())
    print('training_vdata.min():', training_vdata.min())

    print('testing_vdata.max():', testing_vdata.max())
    print('testing_vdata.min():', testing_vdata.min())

    print('training_fdata.max():', training_fdata.max())
    print('training_fdata.min():', training_fdata.min())

    print('testing_fdata.max():', testing_fdata.max())
    print('testing_fdata.min():', testing_fdata.min())

if __name__ == '__main__':
    data_min_max_checker()

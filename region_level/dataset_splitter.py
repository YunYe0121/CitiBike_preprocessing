import numpy as np

def dataset_splitter():

    vdata = np.load('npy_files/vdata.npy')
    fdata = np.load('npy_files/fdata.npy')

    print('vdata.shape:')
    print(vdata.shape)
    print('fdata.shape:')
    print(fdata.shape)

    need_range = 60 * 48

    vdata = vdata[: need_range]
    fdata = fdata[:, : need_range]

    training_dataset_range = 40 * 48

    # vdata
    training_vdata = vdata[: training_dataset_range]
    testing_vdata = vdata[training_dataset_range :]
    # fdata
    training_fdata = fdata[:, : training_dataset_range]
    testing_fdata = fdata[:, training_dataset_range :]

    print('training_vdata.shape:', training_vdata.shape)
    print('testing_vdata.shape:', testing_vdata.shape)
    print('training_fdata.shape:', training_fdata.shape)
    print('testing_fdata.shape:', testing_fdata.shape)

    np.save('npy_files/training_vdata.npy', training_vdata)
    np.save('npy_files/testing_vdata.npy', testing_vdata)
    np.save('npy_files/training_fdata.npy', training_fdata)
    np.save('npy_files/testing_fdata.npy', testing_fdata)

if __name__ == '__main__':
    dataset_splitter()

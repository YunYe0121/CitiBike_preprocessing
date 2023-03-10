import numpy as np

def dataset_splitter():

    scalar_inflow_and_outflow = np.load('npy_files/scalar_inflow_and_outflow.npy')
    scalar_volume = np.load('npy_files/scalar_volume.npy')
    grid_inflow_and_outflow = np.load('npy_files/grid_inflow_and_outflow.npy')
    grid_volume = np.load('npy_files/grid_volume.npy')

    print('scalar_inflow_and_outflow.shape:')
    print(scalar_inflow_and_outflow.shape)
    print('scalar_volume.shape:')
    print(scalar_volume.shape)
    print('grid_inflow_and_outflow.shape:')
    print(grid_inflow_and_outflow.shape)
    print('grid_volume.shape:')
    print(grid_volume.shape)

    need_range = 60 * 48

    scalar_inflow_and_outflow = scalar_inflow_and_outflow[ : need_range]
    scalar_volume = scalar_volume[ : need_range]
    grid_inflow_and_outflow = grid_inflow_and_outflow[ : need_range]
    grid_volume = grid_volume[ : need_range]

    training_dataset_range = 40 * 48

    # scalar_inflow_and_outflow
    training_scalar_inflow_and_outflow = scalar_inflow_and_outflow[ : training_dataset_range]
    testing_scalar_inflow_and_outflow = scalar_inflow_and_outflow[training_dataset_range : ]
    # scalar_volume
    training_scalar_volume = scalar_volume[ : training_dataset_range]
    testing_scalar_volume = scalar_volume[training_dataset_range : ]
    # grid_inflow_and_outflow
    training_grid_inflow_and_outflow = grid_inflow_and_outflow[ : training_dataset_range]
    testing_grid_inflow_and_outflow = grid_inflow_and_outflow[training_dataset_range : ]
    # grid_volume
    training_grid_volume = grid_volume[ : training_dataset_range]
    testing_grid_volume = grid_volume[training_dataset_range : ]

    print('training_scalar_inflow_and_outflow.shape:', training_scalar_inflow_and_outflow.shape)
    print('testing_scalar_inflow_and_outflow.shape:', testing_scalar_inflow_and_outflow.shape)
    print('training_scalar_volume.shape:', training_scalar_volume.shape)
    print('testing_scalar_volume.shape:', testing_scalar_volume.shape)
    print('training_grid_inflow_and_outflow.shape:', training_grid_inflow_and_outflow.shape)
    print('testing_grid_inflow_and_outflow.shape:', testing_grid_inflow_and_outflow.shape)
    print('training_grid_volume.shape:', training_grid_volume.shape)
    print('testing_grid_volume.shape:', testing_grid_volume.shape)

    np.save('npy_files/training_scalar_inflow_and_outflow.npy', training_scalar_inflow_and_outflow)
    np.save('npy_files/testing_scalar_inflow_and_outflow.npy', testing_scalar_inflow_and_outflow)
    np.save('npy_files/training_scalar_volume.npy', training_scalar_volume)
    np.save('npy_files/testing_scalar_volume.npy', testing_scalar_volume)
    np.save('npy_files/training_grid_inflow_and_outflow.npy', training_grid_inflow_and_outflow)
    np.save('npy_files/testing_grid_inflow_and_outflow.npy', testing_grid_inflow_and_outflow)
    np.save('npy_files/training_grid_volume.npy', training_grid_volume)
    np.save('npy_files/testing_grid_volume.npy', testing_grid_volume)

if __name__ == '__main__':
    dataset_splitter()

import numpy as np
import pandas as pd

def data_min_max_checker():

    major_flow_station_info_df = pd.read_csv( 'csv_files/major_flow_station_info.csv' )
    print(major_flow_station_info_df)

    major_flow_df = pd.read_csv( 'csv_files/major_flow.csv' )
    print(major_flow_df)

    scalar_inflow_and_outflow = np.load('npy_files/scalar_inflow_and_outflow.npy')
    scalar_volume = np.load('npy_files/scalar_volume.npy')
    grid_inflow_and_outflow = np.load('npy_files/grid_inflow_and_outflow.npy')
    grid_volume = np.load('npy_files/grid_volume.npy')

    training_scalar_inflow_and_outflow = np.load('npy_files/training_scalar_inflow_and_outflow.npy')
    testing_scalar_inflow_and_outflow = np.load('npy_files/testing_scalar_inflow_and_outflow.npy')

    training_scalar_volume = np.load('npy_files/training_scalar_volume.npy')
    testing_scalar_volume = np.load('npy_files/testing_scalar_volume.npy')

    training_grid_inflow_and_outflow = np.load('npy_files/training_grid_inflow_and_outflow.npy')
    testing_grid_inflow_and_outflow = np.load('npy_files/testing_grid_inflow_and_outflow.npy')

    training_grid_volume = np.load('npy_files/training_grid_volume.npy')
    testing_grid_volume = np.load('npy_files/testing_grid_volume.npy')

    print('scalar_inflow_and_outflow.shape:')
    print(scalar_inflow_and_outflow.shape)
    print('scalar_volume.shape:')
    print(scalar_volume.shape)
    print('grid_inflow_and_outflow.shape:')
    print(grid_inflow_and_outflow.shape)
    print('grid_volume.shape:')
    print(grid_volume.shape)

    print()
    print('training_scalar_inflow_and_outflow.max():', training_scalar_inflow_and_outflow.max())
    print('training_scalar_inflow_and_outflow.min():', training_scalar_inflow_and_outflow.min())
    print()
    print('testing_scalar_inflow_and_outflow.max():', testing_scalar_inflow_and_outflow.max())
    print('testing_scalar_inflow_and_outflow.min():', testing_scalar_inflow_and_outflow.min())
    print()
    print('training_scalar_volume.max():', training_scalar_volume.max())
    print('training_scalar_volume.min():', training_scalar_volume.min())
    print()
    print('testing_scalar_volume.max():', testing_scalar_volume.max())
    print('testing_scalar_volume.min():', testing_scalar_volume.min())
    print()
    print('training_grid_inflow_and_outflow.max():', training_grid_inflow_and_outflow.max())
    print('training_grid_inflow_and_outflow.min():', training_grid_inflow_and_outflow.min())
    print()
    print('testing_grid_inflow_and_outflow.max():', testing_grid_inflow_and_outflow.max())
    print('testing_grid_inflow_and_outflow.min():', testing_grid_inflow_and_outflow.min())
    print()
    print('training_grid_volume.max():', training_grid_volume.max())
    print('training_grid_volume.min():', training_grid_volume.min())
    print()
    print('testing_grid_volume.max():', testing_grid_volume.max())
    print('testing_grid_volume.min():', testing_grid_volume.min())

if __name__ == '__main__':
    data_min_max_checker()

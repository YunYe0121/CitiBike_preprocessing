import numpy as np

def data_min_max_checker():

    POI = np.load('npy_files/POI.npy')

    print('POI.max():', POI.max())
    print('POI.min():', POI.min())

if __name__ == '__main__':
    data_min_max_checker()
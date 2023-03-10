import numpy as np
import pandas as pd

def scalar_array_generator():

    start_month = 7
    end_month = 8
    filter_num = 100
    grid_side_length = 7
    time_slot_num = (31 + 31) * 48

    # station_info
    station_info_df = pd.read_csv('csv_files/station_info.csv')
    print(station_info_df)

    station_name_list = station_info_df['station_name'].tolist()
    station_id_list = station_info_df['station_id'].tolist()
    station_lat_list = station_info_df['station_lat'].tolist()
    station_lng_list = station_info_df['station_lng'].tolist()

    # major_flow_station_info
    major_flow_station_info_df = pd.read_csv('csv_files/major_flow_station_info.csv')
    major_flow_station_name_list = major_flow_station_info_df['station_name'].tolist()
    major_flow_station_id_list = major_flow_station_info_df['station_id'].tolist()
    major_flow_station_index_list = major_flow_station_info_df['index'].tolist()
    major_flow_station_lat_list = []
    major_flow_station_lng_list = []
    for major_flow_station_index, major_flow_station_record in major_flow_station_info_df.iterrows():
        t_i = major_flow_station_record['index']
        major_flow_station_lat_list.append( station_lat_list[t_i] )
        major_flow_station_lng_list.append( station_lng_list[t_i] )

    # arriving_and_deaprting
    arriving_and_deaprting = np.load('npy_files/arr_and_dep.npy')
    print('arriving_and_deaprting:')
    print(arriving_and_deaprting)
    print('arriving_and_deaprting.shape:')
    print(arriving_and_deaprting.shape)

    # rebal_flow
    rebal_flow = np.load('npy_files/rebal_flow.npy')
    print('rebal_flow:')
    print(rebal_flow)
    print('rebal_flow.shape:')
    print(rebal_flow.shape)

    major_flow_df = pd.read_csv('csv_files/major_flow.csv')
    major_flow_df['Unnamed: 0'] = major_flow_df['Unnamed: 0'].astype(str)

    # scalar_inflow_and_outflow
    # 0 is inflow / arriving, 1 is outflow / departing
    scalar_inflow_and_outflow = np.zeros( (time_slot_num, filter_num * 2, 2), dtype = 'int32' )

    # scalar_volume_diff
    scalar_volume_diff = np.zeros((time_slot_num, filter_num * 2, 1), dtype = 'int32')

    # scalar_volume
    scalar_volume = np.zeros((time_slot_num, filter_num * 2, 2), dtype = 'int32')

    for time_slot_index in range(time_slot_num):
        print('time_slot_index:', time_slot_index)
        for current_station_index in range(filter_num * 2):

            # arriving / inflow
            scalar_inflow_and_outflow[time_slot_index, current_station_index, 0] = arriving_and_deaprting[time_slot_index, major_flow_station_index_list[current_station_index], 0]
            arriving_num = arriving_and_deaprting[time_slot_index, major_flow_station_index_list[current_station_index], 0] + rebal_flow[time_slot_index, major_flow_station_index_list[current_station_index], 0]
            
            # departing / outflow
            scalar_inflow_and_outflow[time_slot_index, current_station_index, 1] = arriving_and_deaprting[time_slot_index, major_flow_station_index_list[current_station_index], 1]
            departing_num = arriving_and_deaprting[time_slot_index, major_flow_station_index_list[current_station_index], 1] + rebal_flow[time_slot_index, major_flow_station_index_list[current_station_index], 1]
            
            # volume_diff calculation
            scalar_volume_diff[time_slot_index, current_station_index, 0] = (arriving_num - departing_num)

    initial_volume = 0
    for i in range(filter_num * 2):
        scalar_volume[0, i, 0] = initial_volume

    for i in range(time_slot_num):
        for j in range(filter_num * 2):
            scalar_volume[i, j, 1] = (scalar_volume[i, j, 0] + scalar_volume_diff[i, j, 0])
            if i < time_slot_num - 1:
                scalar_volume[i + 1, j, 0] = scalar_volume[i, j, 1]

    # data wash for scalar_volume
    print( scalar_volume[:, :, 1].max() )
    print( scalar_volume[:, :, 1].min() )
    print( scalar_volume.shape )

    print('scalar_inflow_and_outflow:')
    print(scalar_inflow_and_outflow)
    print('scalar_inflow_and_outflow.shape:')
    print(scalar_inflow_and_outflow.shape)

    print('scalar_volume:')
    print(scalar_volume)
    print('scalar_volume.shape:')
    print(scalar_volume.shape)

    cmp_list = []

    for major_flow_station_index in range(scalar_volume.shape[1]):
        max_value = scalar_volume[:, major_flow_station_index, :].max()
        min_value = scalar_volume[:, major_flow_station_index, :].min()

        diff = max_value - min_value
        ele = (major_flow_station_index, diff)
        cmp_list.append(ele)

    def take_second_element(arg):
        return arg[1]

    cmp_list.sort(key = take_second_element, reverse = True)
    print(cmp_list)

    major_flow_station_index_list, diff_list = zip( *cmp_list )

    major_flow_station_index_list = list(major_flow_station_index_list)
    diff_list = list(diff_list)

    print('major_flow_station_index_list:')
    print(major_flow_station_index_list)
    print('diff_list:')
    print(diff_list)

    abandon_list = major_flow_station_index_list[ : filter_num]
    remaining_list = major_flow_station_index_list[filter_num : ]

    abandon_list.sort()
    remaining_list.sort()

    print('abandon_list:')
    print(abandon_list)
    print('remaining_list:')
    print(remaining_list)

    # remove unneeded data
    scalar_volume = np.delete( scalar_volume, abandon_list, 1 )
    scalar_inflow_and_outflow = np.delete( scalar_inflow_and_outflow, abandon_list, 1 )

    print('scalar_inflow_and_outflow.shape:')
    print(scalar_inflow_and_outflow.shape)
    print('scalar_volume.shape:')
    print(scalar_volume.shape)

    # shift scalar_volume array to let all volume non-negative
    for major_flow_station_index in range(scalar_volume.shape[1]):
        s_min_value = scalar_volume[:, major_flow_station_index, :].min()
        if s_min_value < 0:
            scalar_volume[:, major_flow_station_index, :] += abs(s_min_value)

    # check scalar_inflow_and_outflow and scalar_volume
    print('scalar_volume.max():', scalar_volume.max())
    print('scalar_volume.min():', scalar_volume.min())
    print( scalar_volume.shape )

    print('scalar_inflow_and_outflow.max():', scalar_inflow_and_outflow.max())
    print('scalar_inflow_and_outflow.min():', scalar_inflow_and_outflow.min())
    print( scalar_inflow_and_outflow.shape )

    np.save('npy_files/scalar_inflow_and_outflow.npy', scalar_inflow_and_outflow)
    np.save('npy_files/scalar_volume.npy', scalar_volume)

    # wash for major_flow_station_info.csv
    major_flow_station_info_df = pd.read_csv( 'csv_files/major_flow_station_info.csv' )
    major_flow_station_name_list = major_flow_station_info_df['station_name'].tolist()
    major_flow_station_info_df = major_flow_station_info_df.iloc[remaining_list]
    major_flow_station_info_df.reset_index(drop = True, inplace = True)
    major_flow_station_info_df = major_flow_station_info_df.drop( columns = ['Unnamed: 0'] )

    print(major_flow_station_info_df)
    major_flow_station_info_df.to_csv('csv_files/major_flow_station_info.csv')

    month_name_list = ['July', 'August']

    drop_column_list = []
    for month_name in month_name_list:
        temp_list = [ month_name + '_' + str(ele) for ele in abandon_list]
        drop_column_list += temp_list

    new_index_list = [ major_flow_station_name_list[i] for i in remaining_list ]

    new_column_list = []
    for month_name in month_name_list:
        temp_list = [ month_name + '_' + str(ele) for ele in range(filter_num)]
        new_column_list += temp_list

    # wash for major_flow.csv
    major_flow_df = pd.read_csv( 'csv_files/major_flow.csv' )
    major_flow_df = major_flow_df.iloc[remaining_list]
    major_flow_df = major_flow_df.drop( columns = ['Unnamed: 0'] )
    major_flow_df = major_flow_df.drop( columns = drop_column_list )
    major_flow_df.columns = new_column_list
    major_flow_df.index = new_index_list

    print(major_flow_df)
    major_flow_df.to_csv('csv_files/major_flow.csv')

if __name__ == '__main__':
    scalar_array_generator()

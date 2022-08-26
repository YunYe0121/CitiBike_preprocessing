import csv
import numpy as np
import pandas as pd

def csv_maker():

    train_vdata = np.load('npy_files/training_vdata.npy')
    test_vdata = np.load('npy_files/testing_vdata.npy')

    train_time_slot_num = (40) * 48
    test_time_slot_num = (20) * 48
    w = 10
    h = 20

    for x in range(w):
        for y in range(h):

            region = x * h + y

            if region == 0:

                temp_train_array = train_vdata[:, x, y, :]
                
                new_train_temp_df = pd.DataFrame(temp_train_array, columns = ['arriving', 'departing'])

                time_slot_array = np.arange(train_time_slot_num)
                region_array = np.repeat(region, train_time_slot_num)

                weekday_counter = 3

                weekday_counter -= 1
                weekday_array = np.zeros(train_time_slot_num, dtype = 'int32')
                for day_index in range( len(weekday_array) ):
                    if day_index > 0 and day_index % 48 == 0:
                        weekday_counter = ( weekday_counter + 1) % 7
                    weekday_array[day_index] = weekday_counter
                weekday_array += 1

                time_slot_and_region_value_df = pd.DataFrame({'time_slot': time_slot_array, 'region': region_array})

                new_time_slot_and_region_value_df = time_slot_and_region_value_df.merge( pd.DataFrame(weekday_array, columns = ['weekday']), how = 'inner', left_index = True, right_index = True)
                new_time_slot_and_region_value_df = new_time_slot_and_region_value_df.reindex( columns = ['region', 'time_slot', 'weekday'] )

                train_final_df = new_time_slot_and_region_value_df.merge(new_train_temp_df, how = 'inner', left_index = True, right_index = True)

            else:

                temp_train_array = train_vdata[:, x, y, :]
                
                new_train_temp_df = pd.DataFrame(temp_train_array, columns = ['arriving', 'departing'])

                time_slot_array = np.arange(train_time_slot_num)
                region_array = np.repeat(region, train_time_slot_num)

                weekday_counter = 3

                weekday_counter -= 1
                weekday_array = np.zeros(train_time_slot_num, dtype = 'int32')
                for day_index in range( len(weekday_array) ):
                    if day_index > 0 and day_index % 48 == 0:
                        weekday_counter = ( weekday_counter + 1) % 7
                    weekday_array[day_index] = weekday_counter
                weekday_array += 1

                time_slot_and_region_value_df = pd.DataFrame({'time_slot': time_slot_array, 'region': region_array})

                new_time_slot_and_region_value_df = time_slot_and_region_value_df.merge( pd.DataFrame(weekday_array, columns = ['weekday']), how = 'inner', left_index = True, right_index = True)
                new_time_slot_and_region_value_df = new_time_slot_and_region_value_df.reindex( columns = ['region', 'time_slot', 'weekday'] )

                final_temp_df = new_time_slot_and_region_value_df.merge(new_train_temp_df, how = 'inner', left_index = True, right_index = True)
                train_final_df = pd.concat([train_final_df, final_temp_df])

    train_final_df.reset_index(drop = True, inplace = True)
    print('train_final_df:')
    print(train_final_df)

    for x in range(w):
        for y in range(h):

            region = x * h + y

            if region == 0:

                temp_test_array = test_vdata[:, x, y, :]
                
                new_test_temp_df = pd.DataFrame(temp_test_array, columns = ['arriving', 'departing'])

                time_slot_array = np.arange(test_time_slot_num)
                region_array = np.repeat(region, test_time_slot_num)

                weekday_counter = 1

                weekday_counter -= 1
                weekday_array = np.zeros(test_time_slot_num, dtype = 'int32')
                for day_index in range( len(weekday_array) ):
                    if day_index > 0 and day_index % 48 == 0:
                        weekday_counter = ( weekday_counter + 1) % 7
                    weekday_array[day_index] = weekday_counter
                weekday_array += 1

                time_slot_and_region_value_df = pd.DataFrame({'time_slot': time_slot_array, 'region': region_array})

                new_time_slot_and_region_value_df = time_slot_and_region_value_df.merge( pd.DataFrame(weekday_array, columns = ['weekday']), how = 'inner', left_index = True, right_index = True)
                new_time_slot_and_region_value_df = new_time_slot_and_region_value_df.reindex( columns = ['region', 'time_slot', 'weekday'] )

                test_final_df = new_time_slot_and_region_value_df.merge(new_test_temp_df, how = 'inner', left_index = True, right_index = True)

            else:

                temp_test_array = test_vdata[:, x, y, :]
                
                new_test_temp_df = pd.DataFrame(temp_test_array, columns = ['arriving', 'departing'])

                time_slot_array = np.arange(test_time_slot_num)
                region_array = np.repeat(region, test_time_slot_num)

                weekday_counter = 1

                weekday_counter -= 1
                weekday_array = np.zeros(test_time_slot_num, dtype = 'int32')
                for day_index in range( len(weekday_array) ):
                    if day_index > 0 and day_index % 48 == 0:
                        weekday_counter = ( weekday_counter + 1) % 7
                    weekday_array[day_index] = weekday_counter
                weekday_array += 1

                time_slot_and_region_value_df = pd.DataFrame({'time_slot': time_slot_array, 'region': region_array})

                new_time_slot_and_region_value_df = time_slot_and_region_value_df.merge( pd.DataFrame(weekday_array, columns = ['weekday']), how = 'inner', left_index = True, right_index = True)
                new_time_slot_and_region_value_df = new_time_slot_and_region_value_df.reindex( columns = ['region', 'time_slot', 'weekday'] )

                final_temp_df = new_time_slot_and_region_value_df.merge(new_test_temp_df, how = 'inner', left_index = True, right_index = True)
                test_final_df = pd.concat([test_final_df, final_temp_df])

    test_final_df.reset_index(drop = True, inplace = True)
    print('test_final_df:')
    print(test_final_df)

    train_final_df.to_csv('csv_files/training.csv')
    test_final_df.to_csv('csv_files/testing.csv')

if __name__ == '__main__':
    csv_maker()

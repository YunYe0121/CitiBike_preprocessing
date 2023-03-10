import json

def type_collector():

    all_type_list = set()

    station_num = 1072

    for index in range(1, station_num + 1):

        print('%d / %d' % (index, station_num))
        
        with open('json_files/s_' + str(index) + '.json', encoding = 'UTF-8') as f:
            data = json.load(f)

        for i, result in enumerate(data['results']):
            if 'types' in result: 
                for type in result['types']:
                    all_type_list.add(type)

    print('all_type_list_num:', len(all_type_list))
    print('all_type_list:')
    print(all_type_list)

    all_type_dict = {}
    for type in all_type_list:
        all_type_dict[type] = ''

    print('all_type_dict:')
    print(all_type_dict)

    output_filename = 'json_files/all_type_dict.json'

    with open(output_filename, 'w', encoding = 'UTF-8') as f:
        for type, empty_string in all_type_dict.items():
            print("'" + type + "'" + ' : ' + "'" + empty_string + "',", file = f)

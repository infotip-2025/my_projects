import os
import re


def read_files_to_list(directory_full_path):
    line_by_line = list()
    line_by_line_user_names_only = list()

    # file cont just informational if needed
    file_count = 0

    # open next available file
    for file_name in os.listdir(directory_full_path):
        try:
            # if file can be opened open it if not - print a message
            with open(
                    os.path.join(directory_full_path, file_name),
                    'r', encoding="utf-8"
                    ) as f:
                time_txt = ''
                date_txt = ''
                for line in f:
                    # print(type(line),line)
                    # print(line, end='')
                    line = re.sub(' kcal', 'kcal', line)
                    try:
                        position_of_colon = line.index(':')
                        column_name = line[:position_of_colon]
                        line_data = line[position_of_colon:]
                        position_of_first_space = line_data.index(' ')
                        data_value = line_data[1:position_of_first_space]
                        data_value = re.sub(r'[^0-9\.\:]', '', data_value)
                        data_description = \
                            line_data[position_of_first_space:].strip()
                        # if this is the time and date line we set variables
                        # to add as first colmuns to other lines read
                        if column_name == 'Time':
                            time_txt = data_value
                            date_txt = data_description
                        else:  # if it was a data (not a date/time line)
                            # we append it to our list
                            
                            # retrieve: (3 or 4 letters from line beginning) (a comma) (anything else left)
                            # then return only (3 or 4 letters from line beginning)
                            date_txt_day_name = re.sub(r'(^[a-zA-Z]{3,4})(,)(.*)',r'\1',date_txt)   
                            # then return only (anything else left)
                            date_txt_date = re.sub(r'(^[a-zA-Z]{3,4})(,)(.*)',r'\3',date_txt)
                            
                            # retrive (all non-spaces at the begining of the line) (spaces) (anything after spaces)
                            # then return only (all non-spaces at the begining of the line)
                            data_description_symbol = re.sub(r'([^\s]+)([\s]+)([^\s]+)(.*$)',r'\1',data_description)
                            # then return only (anything after spaces)
                            data_description_txt = re.sub(r'([^\s]+)([\s]+)([^\s]+)(.*$)',r'\3\4',data_description)
                            
                            # append required data as a new line 
                            line_by_line.append(
                                (date_txt_day_name, date_txt_date, time_txt, column_name, data_value, data_description_symbol, data_description_txt)
                                )
                    except Exception:
                        # it was not a data line - user name in the line
                        # user name + some info about the 'data list' appended 
                        # to 'information list'
                        line_by_line_user_names_only.append(
                            f'{"-"*10}> {file_name}, Linii mod 10: {len(line_by_line) % 10}, <{"-"*10}'
                            )
                file_count += 1
        # print a message if file could not be opened
        except OSError as e:
            print('File:', file_name, 'cannot be opened. Error:', e)
    return line_by_line, file_count, line_by_line_user_names_only


def print_data(data_container):
    if isinstance(data_container, list):
        for line in data_container:
            print(line)
    else:
        print('Data container is of not valid type. Use e.g. a list.')

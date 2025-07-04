import os
import re

# setup the directory path
drive = 'u:'
path_a = 'OneDrive'
path_b = 'DRIVE_GOOGLE'
path_c = 'Adoric health'
full_path = os.path.join(drive, '/', path_a, path_b, path_c)

# pick current dir - not needed for this purpose
# and change working dir to the required one
current_dir = os.getcwd()
os.chdir(full_path)


# print(full_path)

def read_files_to_list(directory_full_path):
    line_by_line = list()

    # file cont just informational if needed
    file_count = 0 

    # open next available file
    for file_name in os.listdir(full_path):
        try:
            # if file can be opened open it if not - print a message
            with open(
                    os.path.join(full_path, file_name),
                    'r', encoding="utf-8"
                    ) as f:
                for line in f:
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
                        line_by_line.append(
                            (column_name, data_value, data_description)
                            )
                    except Exception:
                        line_by_line.append(
                            ('-'*10, file_name, len(line_by_line) % 10)
                            )
                file_count += 1
        # print a message if file could not be opened
        except OSError as e:
            print('File:', file_name, 'cannot be opened. Error:', e)
    return line_by_line, file_count

def print_data (data_container):
    if isinstance(data_container,list):
        for line in data_container:
            print(line)
    else:
        print('Data container is of not valid type. Use e.g. a list.')

data_line_by_line, numer_of_files = read_files_to_list(full_path)

print_data(data_line_by_line)


print('Number of processed files:', numer_of_files)


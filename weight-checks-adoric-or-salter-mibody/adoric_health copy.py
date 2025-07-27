import os

drive = 'u:\\'
path_a = 'OneDrive'
path_b = 'DRIVE_GOOGLE'
path_c = 'Adoric health'
full_path = os.path.join(drive, path_a, path_b, path_c)

current_dir = os.getcwd()
os.chdir(full_path)

print(full_path)
line_by_line = list()

# for file_name in os.listdir(full_path):
#     os.close(os.path.join(full_path, file_name))
file_count = 0
for file_name in os.listdir(full_path):
    line_by_line.append('-'*30)
    line_by_line.append(file_name)
    try:
        with open(
                os.path.join(full_path, file_name),
                'r', encoding="utf-8"
                ) as f:
            for line in f.read():
                print(line, end='')
                #line_by_line.append(line)
            file_count += 1

    except OSError as e:
        print('File:', file_name, 'cannot be opened. Error:', e)

print('Number of processed files:', file_count)
print('Current working directory:', os.getcwd())
os.chdir(current_dir)
print('Current working directory:', os.getcwd())
for line in line_by_line:
    print(line)

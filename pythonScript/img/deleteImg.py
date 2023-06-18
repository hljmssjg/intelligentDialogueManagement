import os



folder_path = '//pythonScript/img'
current_file = os.path.basename(__file__)

for filename in os.listdir(folder_path):
    if filename == current_file:
        continue

    file_path = os.path.join(folder_path, filename)
    if filename not in ['__init__.py', 'resized_memory.png']:
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            os.rmdir(file_path)
        else:
            print('NO')

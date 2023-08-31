#check if the file exists
import os

directory_path = "C:/Users/ADMIN/Desktop/code/python/TTS/testt/crop/019db6d0-1dd7-466a-b169-13cf379f12a3"

if os.path.exists(directory_path) and os.path.isdir(directory_path):
    files = [item for item in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, item))]
    
    print("Number of files:", len(files))
    if files:
        print("List of file names:")
        for file_name in files:
            print(file_name)
    else:
        print("No files found in the directory.")
else:
    print("The directory does not exist.")

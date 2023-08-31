#check if the folder exists
import os

directory_path = "C:/Users/ADMIN/Desktop/code/python/TTS/testt/crop/a"

if os.path.exists(directory_path) and os.path.isdir(directory_path):
    folders = [item for item in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, item))]
    
    print("Number of folders:", len(folders))
    if folders:
        print("List of folder names:")
        for folder_name in folders:
            print(folder_name)
    else:
        print("No folders found in the directory.")
else:
    print("The directory does not exist.")
import shutil
import os

path = os.getcwd() + "/result"
shutil.rmtree(path)
print("Directory removed successfully")

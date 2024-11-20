import shutil
from pathlib import Path
import os

#刪除並建立空資料夾
def deleteAllfile(path): 
    # 目錄路徑
    file = Path(path)
    shutil.rmtree(file)
    buildFolder(path)
    
def buildFolder(path):
    os.mkdir(path)


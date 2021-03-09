import os
import shutil
import json
import time
from pathlib import Path

DIRECTORIES = {
    "HTML": [".html5", ".html", ".htm", ".xhtml"],
    "OSU":[".osk", ".osz"],
    "IMAGES": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg",
               ".heif", ".psd"],
    "VIDEOS": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng",
               ".qt", ".mpg", ".mpeg", ".3gp", ".mkv"],
    "DOCUMENTS": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods",
                  ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
                  ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt",
                  "pptx"],
    "ARCHIVES": [".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z",
                 ".dmg", ".rar", ".xar", ".zip"],
    "AUDIO": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3",
              ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"],
    "PLAINTEXT": [".txt", ".in", ".out"],
    "DOCUMENTS": [".pdf",".docx"],
    "PYTHON": [".py"],
    "XML": [".xml"],
    "EXE": [".exe"],
    "SHELL": [".sh"]
}



class manager:
    def __init__(self, dir_dict):
        """Constructor

        Args:
            dir_dict (dict): [Dictionary of file extensions with folders]
        """
        self.download_path = ''
        self.directories = dir_dict
        self.file_formats = {file_format: directory
                for directory, file_formats in self.directories.items()
                for file_format in file_formats} 
        with open('config.json') as f:
            self.config = json.load(f)
        self.schedule_repeat = int(self.config["do_every"])
        self.download_path = self.config['downloads_folder'] + '\\'
        self.schedule_repeat = int(self.config["do_every"])

    def setup(self):    
        """Setup our program to run
        """
        for directory in self.directories.keys():
            path = os.path.join(self.download_path + directory)
            try:
                os.mkdir(path)
            except FileExistsError:
                pass
        try:
            os.mkdir(self.download_path + "OTHER")
        except FileExistsError:
            pass
        try:
            os.mkdir(self.download_path + "FOLDERS")
        except FileExistsError:
            pass
    
    def run(self):
        """Main function to run our program
        """
        print('running')
        for file in os.listdir(self.download_path):
            file_suffix = Path(file).suffix # file extension
            if not file_suffix: #  if there is no file suffix then it must be a folder
                if file not in self.directories.keys() and file.lower() not in ["other", "folders"]: # avoid recursive lol
                    file_path = os.path.join(self.download_path, file)
                    move_to = os.path.join(self.download_path, "FOLDERS")
                    try:
                        shutil.move(file_path, move_to) # move folder 
                        print(f'moved {file} to {move_to}')
                    except:
                        pass
            else:
                file_path = os.path.join(self.download_path, file)
                if file_suffix in self.file_formats:
                    move_to = os.path.join(self.download_path, self.file_formats[file_suffix])
                    try:
                        shutil.move(file_path, move_to)
                        print(f'moved {file} to {move_to}')
                    except:
                        pass
                else:
                    move_to = os.path.join(self.download_path, "OTHER") # we dont have file suffix in our dict
                    try:
                        shutil.move(file_path, move_to)
                        print(f'moved {file} to {move_to}')
                    except:
                        pass

with open('config.json') as f:
    config = json.load(f)

dl_manager = manager(DIRECTORIES)
dl_manager.setup()
while 1:
    dl_manager.run()
    time.sleep(config["do_every"])
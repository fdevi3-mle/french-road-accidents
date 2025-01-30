import json
import os.path
from datetime import datetime
from enum import Enum
from pathlib import Path

##Constants & FILEPATHS
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__)) ## src
ROOT_PATH = os.path.dirname(CURRENT_PATH)
DATA_PATH =  os.path.join(ROOT_PATH, 'data')
MODEL_PATH =  os.path.join(ROOT_PATH,'models')
NOTEBOOK_PATH = os.path.join(ROOT_PATH, 'notebooks')
SRC_PATH = os.path.join(ROOT_PATH,'src')

##DATA FILE
INPUT_PATH = os.path.join(DATA_PATH,'input')
INPUT_PARQUET = os.path.join(INPUT_PATH,'input_0.parquet')

OUTPUT_PATH = os.path.join(DATA_PATH,'output')

CSV_EXTENSION=  '.csv'
PARQUET_EXTENSION = '.parquet'
HTML = '.html'
PNG = '.png'
JPG = '.jpg'


##LAT & LONG : BORDERS
LAT_MIN = 40.0
LAT_MAX = 60.0
LON_MIN = -10.0
LON_MIN = 10.0

VERSION = '0.0.0'


class CategoryBaseEnum(Enum):
    @classmethod
    def Name(cls):
        return f"{cls.__name__}"
    @classmethod
    def IsCategory(cls):
        return True if len(cls.__members__) > 0 else False
    @classmethod
    def get_description(cls):
        return cls.__doc__ or "No description available"
    @classmethod
    def to_dict(cls):
        return {member.name:member.value for member in cls}
    @classmethod
    def to_json(cls, indent=4):
        return json.dumps(cls.to_dict(), indent=indent)


class FileTypeEnum(Enum):
    @classmethod
    def Name(cls):
        return f"{cls.__name__}"
    @classmethod
    def get_description(cls):
        return cls.__doc__ or "No description available"
    @classmethod
    def to_dict(cls):
        return {member.name:member.value.to_dict() for member in cls}


class ExtensionMethods:
    @staticmethod
    def generate_filename(filename=None,extension=None):
        current_datetime = datetime.now()
        f = current_datetime.strftime("%Y_%m_%d_%H%M")
        if (filename is None) or (extension is None):
            return str(f)
        else:
            stitched_f = str(filename)+"_"+str(f)+"."+str(extension)
            return str(stitched_f)

    @staticmethod
    def get_file_name_without_extension(filename):
        if filename is None:
            return "Provide a file"
        return Path(filename).stem

    @staticmethod
    def get_all_files(dirpath=DATA_PATH,extension='.parquet'):
        _all_files ={}
        file_list = os.listdir(dirpath)
        for file in file_list:
            filepath = os.path.join(dirpath,file)
            if file.endswith(extension):
                _all_files[file] = filepath

        return _all_files

    @staticmethod
    def create_parquet(data=None,filename='',filepath=OUTPUT_PATH):
        if data is None:
            raise ValueError("Data can't be None for Parquet Creation")
        obj_cols = data.select_dtypes(include=['object','categorical']).columns
        for col in obj_cols:
            data[col] = data[col].astype(str)
        if not os.path.exists(filepath):
            os.makedirs(filepath) ## a bit of cheating
        _full_path = os.path.join(filepath,filename)
        data.to_parquet(filepath, engine='pyarrow', compression="zstd", compression_level=10, index=False)
        print(f"\n Finished Saving parquet to: {filepath}")


## Lets test
if __name__ == "__main__":
    print(f"ROOT_PATH: {ROOT_PATH}")
    print(f"CURRENT_PATH: {CURRENT_PATH}")
    print(f"DATA_PATH: {DATA_PATH}")
    print(f"VERSION: {VERSION}")
    print(f"SRC_PATH: {SRC_PATH}")
    print(f"OUTPUT_PATH: {OUTPUT_PATH}")
    print(f"FileName generated {ExtensionMethods.generate_filename("test",'jpg')}")
    print(f"FileName generated {ExtensionMethods.get_all_files(INPUT_PATH)}")

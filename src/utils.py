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


## Lets test
if __name__ == "__main__":
    print(f"ROOT_PATH: {ROOT_PATH}")
    print(f"CURRENT_PATH: {CURRENT_PATH}")
    print(f"DATA_PATH: {DATA_PATH}")
    print(f"VERSION: {VERSION}")
    print(f"SRC_PATH: {SRC_PATH}")
    print(f"FileName generated {ExtensionMethods.generate_filename("test",'jpg')}")
import pytest
import pandas as pd
import pandera as pa
from pandera import Column
from pandas import Int32Dtype
from unittest.mock import patch

from src.franums import RoadAccidentEnum
from src.utils import INPUT_PARQUET

## Fiztures ##
@pytest.fixture
def synthetic_good_data():
    mega_dic = RoadAccidentEnum.mega_dictionary()
    _good_data = {}
    for index, value in mega_dic.items():
        if mega_dic[index][1]:
            _good_data[index] = [list(value[0].keys())[1]] ## take the first key
        else:
            if index == 'vehicle_id':
                _good_data[index] = ["202020202020"]
            if index == 'dob':
                _good_data[index] = [1980]
            if index == 'age':
                _good_data[index] = [45]
            if index == 'datetime':
                _good_data[index] = [pd.to_datetime(1490195805, unit='s')] ##just took it from pd.todatetime example
            if (index == 'lat') or (index == 'long'):
                _good_data[index] = [4.20]
            if index == 'h3':
                _good_data[index] = ['8928308280fffff'] ## took a default value from h3
    return pd.DataFrame(_good_data)


@pytest.fixture
def synthetic_bad_data():
    mega_dic = RoadAccidentEnum.mega_dictionary()
    _bad_data = {}
    for index, value in mega_dic.items():
        if mega_dic[index][1]:
            _bad_data[index] = [list(value[0].keys())[1]] ## take the first key
        else:
            if index == 'vehicle_id':
                _bad_data[index] = ["202020202020"]
            if index == 'dob':
                _bad_data[index] = ["1980"]
            if index == 'age':
                _bad_data[index] = ["cccc"]
            if index == 'datetime':
                _bad_data[index] = [pd.to_datetime(1490195805, unit='s')] ##just took it from pd.todatetime example
            if (index == 'lat') or (index == 'long'):
                _bad_data[index] = ["xxx"]
            if index == 'h3':
                _bad_data[index] = ['8928308280fffff'] ## took a default value from h3
    return pd.DataFrame(_bad_data)



def test_validation_synthetic_good_data(synthetic_good_data):
    data = synthetic_good_data
    mega_dic = RoadAccidentEnum.mega_dictionary()
    columns = {}
    for index, value in mega_dic.items():
        if mega_dic[index][1]:
            columns[index] = Column(str)
        else:
            if index == 'vehicle_id':
                columns[index] = Column(str)
            if (index == 'dob') or (index == 'age'):
                columns[index] = Column(int)
            if index == 'datetime':
                columns[index] = Column(pa.DateTime)
            if (index == 'lat') or (index == 'long'):
                columns[index] = Column(float)
            if index == 'h3':
                columns[index] = Column(str)

    schema = pa.DataFrameSchema(columns=columns)
    print(schema)
    try:
        schema.validate(data, lazy=True)
        print("All validated")
        assert True
    except pa.errors.SchemaErrors as exc:
        print("Schema errors and failure cases:")
        print(exc.failure_cases)
        print("\nDataFrame object that failed validation:")
        print(exc.data)
        assert False ## If it comes here then its false

def test_validation_synthetic_bad_data(synthetic_bad_data):
    data = synthetic_bad_data
    mega_dic = RoadAccidentEnum.mega_dictionary()
    columns = {}
    for index, value in mega_dic.items():
        if mega_dic[index][1]:
            columns[index] = Column(str)
        else:
            if index == 'vehicle_id':
                columns[index] = Column(str)
            if (index == 'dob') or (index == 'age'):
                columns[index] = Column(int)
            if index == 'datetime':
                columns[index] = Column(pa.DateTime)
            if (index == 'lat') or (index == 'long'):
                columns[index] = Column(float)
            if index == 'h3':
                columns[index] = Column(str)

    schema = pa.DataFrameSchema(columns=columns)
    print(schema)
    try:
        schema.validate(data, lazy=True)
        print("All validated")
        assert False ## I should not pass
    except pa.errors.SchemaErrors as exc:
        print("Schema errors and failure cases:")
        print(exc.failure_cases)
        print("\nDataFrame object that failed validation:")
        print(exc.data)
        assert True ## Lol, I failed




def test_data_validation_parquet(filepath=INPUT_PARQUET):
    data = pd.read_parquet(filepath)
    valid_columns = RoadAccidentEnum.to_dict()
    valid_columns = valid_columns.keys()
    data = data[[col for col in data.columns if col in valid_columns]]
    print(data.head(1))

    mega_dic = RoadAccidentEnum.mega_dictionary()
    columns = {}
    for index, value in mega_dic.items():
        if mega_dic[index][1]:
            columns[index] = Column(str)
        else:
            if index == 'vehicle_id':
                columns[index] = Column(str)
            if (index == 'dob') or (index=='age'):
                columns[index] = Column(Int32Dtype())
            if index == 'datetime':
                columns[index] = Column(pa.DateTime)
            if (index=='lat') or (index=='long'):
                columns[index] = Column(float)
            if index == 'h3':
                columns[index] = Column(str)


    schema = pa.DataFrameSchema(columns=columns)
    print(schema)
    try:
        schema.validate(data, lazy=True)
        print("All validated")
        assert True
    except pa.errors.SchemaErrors as exc:
        print("Schema errors and failure cases:")
        print(exc.failure_cases)
        print("\nDataFrame object that failed validation:")
        print(exc.data)
        assert False



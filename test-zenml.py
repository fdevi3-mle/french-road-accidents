import logging
import os.path
from zenml import pipeline, step

from src.utils import CURRENT_PATH, ROOT_PATH, generate_logger, LOG_PATH, generate_random_image


@step  # Just add this decorator
def load_data() -> dict:
    training_data = [[1, 2], [3, 4], [5, 6]]
    labels = [0, 1, 0]
    return {'features': training_data, 'labels': labels}

@step
def train_model(data: dict) -> None:
    total_features = sum(map(sum, data['features']))
    total_labels = sum(data['labels'])
    
    print(f"Trained model using {len(data['features'])} data points. "
          f"Feature sum is {total_features}, label sum is {total_labels}")



def do_something():
    print("HI")
    filepath = os.path.join(LOG_PATH, 'hello.txt')
    with open(filepath, 'w') as f:
        f.write('hello')
    if os.path.exists(LOG_PATH):
        for filename in os.listdir(LOG_PATH):
            filepath = os.path.join(LOG_PATH, filename)
            if os.path.isfile(filepath):
                print(filepath)
    else:
        print(f"The directory '{LOG_PATH}' does not exist.")




@pipeline(enable_cache=False)  # This function combines steps together
def simple_ml_pipeline():
    dataset = load_data()
    train_model(dataset)

if __name__ == "__main__":
    print(f"I am here {os.getcwd()}")
    print(f"My Current Paths is {CURRENT_PATH}")
    print(f"My Root Path is {ROOT_PATH}")
    generate_logger()
    generate_random_image()
    run = simple_ml_pipeline()  # call this to run the pipeline
    do_something()

   






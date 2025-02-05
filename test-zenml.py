import logging
import os.path
from zenml import pipeline, step

from src.utils import CURRENT_PATH, ROOT_PATH, generate_logger


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

@pipeline  # This function combines steps together 
def simple_ml_pipeline():
    dataset = load_data()
    train_model(dataset)

if __name__ == "__main__":
    print(f"I am here {os.getcwd()}")
    print(f"My Current Paths is {CURRENT_PATH}")
    print(f"My Root Path is {ROOT_PATH}")
    generate_logger()
    run = simple_ml_pipeline()  # call this to run the pipeline
   






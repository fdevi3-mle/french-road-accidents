from zenml import pipeline, step


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


@pipeline(enable_cache=True)  # This function combines steps together
def simple_ml_pipeline():
    dataset = load_data()
    train_model(dataset)

def hello():
    print("Hiiii I work")
    simple_ml_pipeline()


if __name__ == "__main__":
    print("Hiiii I work")
    run = simple_ml_pipeline()  # call this to run the pipeline
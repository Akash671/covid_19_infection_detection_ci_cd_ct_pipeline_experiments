import os
from training.train import train_model

def test_train_model():
    model_path, acc = train_model()
    assert os.path.exists(model_path)
    assert acc > 0

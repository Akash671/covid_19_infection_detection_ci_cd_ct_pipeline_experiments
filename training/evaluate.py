import joblib
from sklearn.metrics import accuracy_score, classification_report


def evaluate_model(model_path, X_test, y_test):
    model = joblib.load(model_path)
    preds = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))

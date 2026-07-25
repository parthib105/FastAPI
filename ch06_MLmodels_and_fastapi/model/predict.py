import pickle
import pandas as pd
from pathlib import Path

MODEL_VERSION = '1.0.0'

# Load the serialized model using a path relative to this file
BASE_DIR = Path(__file__).resolve().parent
model_path = BASE_DIR / "trained_model.pkl"

if not model_path.is_file():
    raise FileNotFoundError(
        f"Trained model not found at {model_path}. "
        "Run `python -m ch06_MLmodels_and_fastapi.model.model` to generate it."
    )

with open(model_path, 'rb') as f:
    my_model = pickle.load(f)

# Get class labels from model (important for matching probabilities to class names)
class_labels = my_model.classes_.tolist()

# predict function
def predict_output(user_input: dict):
    input_df: pd.DataFrame = pd.DataFrame([user_input])

    # Predict the class
    predicted_class = my_model.predict(input_df)[0]

    # Get probabilities for all classes
    probabilities = my_model.predict_proba(input_df)[0]
    confidence = max(probabilities)
    
    # Create mapping: {class_name: probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))

    return {
        "predicted_category": predicted_class,
        "confidence": round(confidence, 4),
        "class_probabilities": class_probs
    }
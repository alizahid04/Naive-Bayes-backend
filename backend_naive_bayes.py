from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

def load_model(action):
    if action == "loan":
        model = joblib.load("models_save/naive_bayes_model_loan.pkl")
        le_dict = joblib.load("models_save/feature_encoders_loan.pkl")
        le_target = joblib.load("models_save/target_encoder_loan.pkl")
    elif action == "accident":
        model = joblib.load("models_save/naive_bayes_model_accident.pkl")
        le_dict = joblib.load("models_save/feature_encoders_accident.pkl")
        le_target = joblib.load("models_save/target_encoder_accident.pkl")
    elif action == "animal":
        model = joblib.load("models_save/naive_bayes_model_animal.pkl")
        le_dict = joblib.load("models_save/feature_encoders_animal.pkl")
        le_target = joblib.load("models_save/target_encoder_animal.pkl")
    elif action == "spam":
        model = joblib.load("models_save/naive_bayes_model_spam.pkl")
        le_dict = joblib.load("models_save/feature_encoders_spam.pkl")
        le_target = joblib.load("models_save/target_encoder_spam.pkl")
    else:
        return None, None, None
    return model, le_dict, le_target

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        action = data.get("action")
        if not action:
            return jsonify({"error": "No action specified."}), 400

        features = {k: v for k, v in data.items() if k != "action"}
        new_data = pd.DataFrame([features])

        model, le_dict, le_target = load_model(action)
        if model is None:
            return jsonify({"error": f"No model found for action '{action}'"}), 400

        # Encode features
        for col in new_data.columns:
            if col in le_dict:
                new_data[col] = le_dict[col].transform(new_data[col])

        # Predict
        pred = model.predict(new_data)
        label = le_target.inverse_transform(pred)

        # Get probability for all classes
        probs = model.predict_proba(new_data)
        class_probs = dict(zip(le_target.classes_, probs[0]))
        class_probs_percent = {k: f"{v*100:.2f}%" for k, v in class_probs.items()}

        result = {
            "Prediction": label[0],
            "Probability": class_probs_percent
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Naive Bayes Backend is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
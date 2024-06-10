from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd
import logging


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Cargar el modelo
model = joblib.load('random_forest_model.pkl')
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # Asumiendo que el JSON tiene la misma estructura que los datos de entrenamiento
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    return jsonify({'prediction': int(prediction[0])})


if __name__ == '__main__':
    app.run(debug=True)

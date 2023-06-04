from fastapi import FastAPI
import tensorflow as tf
import h5py

app = FastAPI()
model_paths = {
    "bandeng": "model/bandeng_model_lstm.h5",
    "kembung_lelaki": "model/kembung_lelaki_model_lstm.h5",
    "tenggiri": "model/tenggiri_model_lstm.h5",
    "tongkol_abu": "model/tongkol_abu_model_lstm.h5",
    "tongkol_komo": "model/tongkol_komo_model_lstm.h5",
    # Add more fish types and their corresponding model paths
}

# Load all the models during start
loaded_models = {}

def load_all_models():
    for fish_type, model_path in model_paths.items():
        with h5py.File(model_path, "r") as file:
            model = tf.keras.models.load_model(file)
            loaded_models[fish_type] = model

load_all_models()

# GET /
@app.get("/")
async def root():
    return {"message": "Hello from the price prediction server!"}

# GET /predict/{fish_type}/{date}
@app.get("/predict/{fish_type}/{date}")
async def predict_price(fish_type: str, date: str):
    # Preprocess the input date if necessary
    # Perform any required data manipulation or transformation

    # Make the prediction using the loaded model
    model = loaded_models.get(fish_type)
    if model is None:
        return {"error": "Invalid fish type, currently there's no such fish in the model"}

    prediction = model.predict([date])[0]

    # Return the prediction as a response
    return {"date": date, "predicted_price": float(prediction)}
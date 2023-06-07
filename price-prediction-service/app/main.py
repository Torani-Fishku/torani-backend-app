from fastapi import FastAPI
import tensorflow as tf
import h5py
import pandas as pd
import numpy as np

app = FastAPI()
model_paths = {
    "bandeng": "model/bandeng_model_lstm.h5",
    "kembung_lelaki": "model/kembung_lelaki_model_lstm.h5",
    "tenggiri": "model/tenggiri_model_lstm.h5",
    "tongkol_abu": "model/tongkol_abu_model_lstm.h5",
    "tongkol_komo": "model/tongkol_komo_model_lstm.h5",
    # Add more fish types and their corresponding model paths
}

data_paths = {
    "bandeng": "dataset/bandeng_smoothed_data.csv",
    "kembung_lelaki": "dataset/kembung_lelaki_smoothed_data.csv",
    "tenggiri": "dataset/tenggiri_smoothed_data.csv",
    "tongkol_abu": "dataset/tongkol_abu_smoothed_data.csv",
    "tongkol_komo": "dataset/tongkol_komo_smoothed_data.csv"
}


# Load all the models during start
loaded_models = {}

def load_all_models():
    for fish_type, model_path in model_paths.items():
        with h5py.File(model_path, "r") as file:
            model = tf.keras.models.load_model(file)
            loaded_models[fish_type] = model

load_all_models()

# Load all dataset and preprocess
window_size=8
#loaded_datasets = {}
normalized_datasets = {}
windowed_data= {}
min_max_data={}

def min_max(data,fish_type):
    # Store the min and max price for unscaling later
    data_min = min(data)
    data_max = max(data)
    min_max_data[fish_type]={'Min':data_min,'Max':data_max}

def normal_scaler(data,fish_type):
    # Compute the minimum and maximum values
    data_min, data_max = min_max_data[fish_type]['Min'],min_max_data[fish_type]['Max']
    # Scale the data using the min-max formula
    scaled_data = [(x - data_min) / (data_max - data_min) for x in data]
    return scaled_data

def unscaler(data,fish_type):
    # Unscale the data using the min-max formula
    data_min, data_max = min_max_data[fish_type]['Min'],min_max_data[fish_type]['Max']
    unscaled_data = (data*(data_max-data_min))+data_min
    return unscaled_data

def preprocess_data(data_paths,window_size):
    for fish_type, data_path in data_paths.items():
        df = pd.read_csv(data_path).tail(window_size)
        #loaded_datasets[fish_type] = df
        min_max(df['harga'],fish_type)
        normalized_datasets[fish_type] = normal_scaler(df['harga'],fish_type)

def df_to_X(df, window):
  df_as_np = df.to_numpy()
  X = []
  #y = []
  for i in range(len(df_as_np)-window):
    row = [[a] for a in df_as_np[i:i+window]]
    X.append(row)
    #label = df_as_np[i+window]
    #y.append(label)
  return np.array(X, dtype=float) #, np.array(y, dtype=float)

def windowing_data(dataframes):
    for fish_type, dataframe in dataframes.items():
        windowed_X = df_to_X(dataframe['harga'],window_size)
        windowed_data[fish_type]=windowed_X

preprocess_data(data_paths=data_paths,window_size=window_size)
windowing_data(normalized_datasets)
    
# GET /
@app.get("/")
async def root():
    return {"message": "Hello from the price prediction server!"}

# GET /predict/{fish_type}/{date}
@app.get("/predict/{fish_type}/{date}")
async def predict_price(start_date: str,  fish_type: str, input_data=windowed_data[fish_type],days=7):
    # Preprocess the input date if necessary
    # Perform any required data manipulation or transformation
    predictions_df = pd.DataFrame(columns=['Date', 'Price'])
    # Make the prediction using the loaded model
    model = loaded_models.get(fish_type)
    if model is None:
        return {"error": "Invalid fish type, currently there's no such fish in the model"}

    input_data[fish_type] = input_data[fish_type].to_numpy().reshape(1, -1, 1)
    for i in range(days):
        prediction = model.predict(input_data[fish_type])
        pred_row={'Date': start_date + pd.DateOffset(days=i), 'Price': unscaler(prediction,fish_type)[0][0]}
        predictions_df=predictions_df.append(pred_row, ignore_index=True)
        # Update the input data for the next prediction
        input_data = np.concatenate((input_data, prediction.reshape(1, 1, 1)), axis=1)

    # Return the prediction as a response
    return predictions_df

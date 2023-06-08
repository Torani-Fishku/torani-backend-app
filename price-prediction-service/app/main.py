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
normalized_datasets = {}
date_data = {}
windowed_data= {}
min_max_data= {}

def min_max(data,fish_type):
    # Store the min and max price for unscaling later
    data_min = min(data)
    data_max = max(data)
    min_max_data[fish_type]={'Min':data_min,'Max':data_max}

def normal_scaler(data,fish_type):
    # Compute the minimum and maximum values
    data_min, data_max = min_max_data[fish_type]['Min'],min_max_data[fish_type]['Max']
    # Scale the data using the min-max formula
    scaled_data = (data - data_min) / (data_max - data_min)
    return scaled_data

def unscaler(data,fish_type):
    # Unscale the data using the min-max formula
    data_min, data_max = min_max_data[fish_type]['Min'],min_max_data[fish_type]['Max']
    unscaled_data = (data*(data_max-data_min))+data_min
    return unscaled_data

def fish_date(data,fish_type):
    date=pd.to_datetime(data)
    date_data[fish_type]=date

def preprocess_data(data_paths,window_size):
    # Load and normalize the fish price data
    for fish_type, data_path in data_paths.items():
        df = pd.read_csv(data_path)
        min_max(df['harga'],fish_type)
        fish_date(df['tanggal_input'],fish_type)
        normalized_datasets[fish_type] = normal_scaler(df['harga'],fish_type)

def df_to_X(df, window):
  # Make the tail of the price data to array
  # The array size is in the form of input of LSTM Neural Network
  df_as_np = df.tail(window).to_numpy()
  X = []
  for i in range(len(df_as_np)-window+1):
    row = [[a] for a in df_as_np[i:i+window]]
    X.append(row)
  return np.array(X, dtype=float)

def windowing_data(dictionary):
    #Loop for windowing the data by executing df_to_X function for each fish
    for fish_type, item in dictionary.items():
        windowed_X = df_to_X(item,window_size)
        windowed_data[fish_type]=windowed_X
        
def generate_predictions(n_time, fish_type, window=window_size):
    # Create an empty dataframe to store the predictions
    predictions_df = pd.DataFrame(columns=['Date', 'Price'])
    
    # Load the fish prediction model  
    model = loaded_models.get(fish_type)
    
    # Load the fish price date
    start_date= date_data.get(fish_type).iloc[-1]

    # Reshape the input_data to maintain the original shape for future predictions
    input_data = windowed_data[fish_type].reshape(1, -1, 1)
    
    # Generate predictions for each day ahead
    for i in range(n_time):
        # Prepare the input data for prediction
        input_data_pred = input_data[:, int(-1*window):, :]  # Use the last 8 values for prediction
        
        # Predict the next price using the model
        predicted_price = model.predict(input_data_pred)
        # Add the prediction to the dataframe
        prediction_row = {'Date': start_date + pd.DateOffset(days=i), 'Price': unscaler(predicted_price,fish_type)[0][0]}
        predictions_df = predictions_df.append(prediction_row, ignore_index=True)
        
        # Update the input data for the next prediction
        input_data = np.concatenate((input_data, predicted_price.reshape(1, 1, 1)), axis=1)

    return predictions_df
        
preprocess_data(data_paths=data_paths,window_size=window_size)
windowing_data(normalized_datasets)
    
# GET /
@app.get("/")
async def root():
    return {"message": "Hello from the price prediction server!"}

# GET /predict/{fish_type}/{date}
@app.get("/predict/{fish_type}/{date}")
async def predict_price(date: str,  fish_type: str):

    # Load the model
    model = loaded_models.get(fish_type)
    if model is None:
        return {"error": "Invalid fish type, currently there's no such fish in the model"}

    predictions_df=generate_predictions(n_time=7, fish_type=fish_type)
    #date_predicted=predictions_df[predictions_df['Date']=='2023-02-10']['Date'] #.dt.strftime('%Y-%m-%d').values[0]
    price_predicted=float(predictions_df[predictions_df['Date']==date]['Price'])
    # Return the prediction as a response
    return {'date': date, 'predicted_price': price_predicted}

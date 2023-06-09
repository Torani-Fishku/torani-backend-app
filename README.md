### Torani-Fishku/torani-backend-app
## Fish Price Prediction API

This program predicts fish prices using LSTM machine learning model. We are using PDSPKP fish prices dataset with the date range between 8 - 14 February 2023. The data is pulled from: https://datacenterpds.id/warta-ikan

Using Python 3.9 with FastAPI library.
### How to run this program:

1. Install the dependencies

      ```pip install --no-cache-dir -r requirements.txt```

3. Install Uvicorn

      ```pip install uvicorn```
4. Run the server

      ```uvicorn main:app --host 0.0.0.0 --port 8080```
5.  To test it go to 

      ```http://localhost:8080/predict/{fish_type}/{yyyy-mm-dd}```
  
### Deployed link: 
  
https://price-prediction-api-ui5j6olklq-et.a.run.app/predict/bandeng/2023-02-08

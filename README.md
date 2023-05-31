# Torani-Fishku/torani-backend-app
## Sea Tides API
This program is to fetch sea tides and weather information based on client's coordinate. The data is pulled from:
https://peta-maritim.bmkg.go.id/public_api/perairan.
Using Node.JS v18.15.0 with Express.
### How to run this program:
 
1. ```npm install```
 
2.  ```npm run start```
  
3.  Then the server will start serving request at ```localhost:3000```
  
4.  To test it go to ```http://localhost:3000/location?longitude=<longitude>&latitude=<latitude>```
  
  Example: 
  
  http://localhost:3000/location?longitude=131.782462&latitude=10.220737
  
  response:
  ```{
  "code": "O.01",
  "name": "Samudera Pasifik utara Halmahera bagian utara",
  "issued": "2023-05-31 05:00 UTC",
  "data": [
    {
      "valid_from": "2023-05-31 12:00 UTC",
      "valid_to": "2023-06-01 00:00 UTC",
      "time_desc": "Hari ini",
      "weather": "Berawan",
      "weather_desc": "Pola angin di wilayah Indonesia bagian utara umumnya bergerak dari Selatan - Barat dengan kecepatan angin berkisar 4 &ndash; 22 knot",
      "warning_desc": "NIHIL.",
      "station_remark": "NIHIL.",
      "wave_cat": "Sedang",
      "wave_desc": "1.25 - 2.50 m",
      "wind_from": "Selatan",
      "wind_to": "Barat Daya",
      "wind_speed_min": 5,
      "wind_speed_max": 20
    },
    ... information for the next 3 days
  ]
}

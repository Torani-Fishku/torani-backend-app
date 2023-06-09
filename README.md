### Torani-Fishku/torani-backend-app
## Sea Tides API
This program is to fetch sea tides and weather information based on client's coordinate. The data is pulled from:
https://peta-maritim.bmkg.go.id/public_api/perairan.
Using Node.js v18.15.0.
### How to run this program:
 
1. Install the dependencies

    ```npm install```
 
2.  Run the server

    ```npm run start```
    
3.  To test it go to 
   
    ```http://localhost:3000/location?longitude=<longitude>&latitude=<latitude>```
    
### Deployed link: 
  
https://sea-tides-api-ui5j6olklq-et.a.run.app/location?longitude=106.3981545342644&latitude=-7.185463902800723
  
  response:
  ```{
  "code": "U.03",
  "name": "Perairan selatan Banten",
  "issued": "2023-06-09 05:00 UTC",
  "data": [
    {
      "valid_from": "2023-06-09 12:00 UTC",
      "valid_to": "2023-06-10 00:00 UTC",
      "time_desc": "Hari ini",
      "weather": "Berawan",
      "weather_desc": "Angin di wilayah Selat Sunda bagian Utara umumnya bertiup dari Tmur Laut - Tenggara&nbsp;dengan kecepatan 1 - 08 knot<br />\nAngin di wilayah Selat Sunda bagian Selatan umumnya bertiup dari Timur - Selatan&nbsp;dengan kecepatan 1 - 20 knot<br />\nAngin di wilayah Perairan Selatan Banten umumnya bertiup dari Timur - Selatan dengan kecepatan 1 - 25&nbsp;knot<br />\nAngin di wilayah Samudera Hindia Selatan Banten umumnya bertiup dari Timur - Selatan dengan kecepatan 1 - 25&nbsp;knot",
      "warning_desc": "Waspada gelombang laut dengan ketinggian 2.5 - 4.0 meter di wilayah Selat Sunda bagan Selatan dan Perairan Selatan Banten yang beresiko tinggi terhadap Perahu Nelayan, Kapal Tongkang, dan Kapal Ferry.&nbsp;<br />\nWaspada gelombang laut dengan ketinggian 4.0 - 6.0 meter di wilayah Samudera Hindia Selatan Banten&nbsp;yang beresiko tinggi terhadap semua jenis Kapal.",
      "station_remark": "-",
      "wave_cat": "Tinggi",
      "wave_desc": "2.50 - 4.0 m",
      "wind_from": "Timur",
      "wind_to": "Selatan",
      "wind_speed_min": 1,
      "wind_speed_max": 25
    },
    ....
  ]
}
```


# weewx-davishealthapi
Collect and display station health information from the Davis WeatherLink API

Modified from author uajqq

Weewx service that pulls device health (telemetry) information from Davis Instruments weather sensor(s) - up to 8 and from one DAVIS Airlink. 
I made this extension for users like me who have a WeatherLink Live device, which unfortunately provides no sensor health data over the local API. 
Please note: only a attached DAVIS VantageVUE  reports values for supercapVolt, solarVolt and txBattery

The code makes two API calls per archive period: 
one to the "current" v2 API, which contains values like the console battery status and firmware version, 
and another to the "historical" v2 API, which contains most of the sensor's health telemetry like signal strength, signal quality, 
solar cell voltage, and so on.

The data are stored in their own database, since most of the fields don't exist within the default weewx database. 

Please note: most of the data is pulled from the "Historic Data" API, which 
requires a paid monthly subscription from Davis to use (starting at about $4/month). 
See here: https://weatherlink.github.io/v2-api/data-permissions

## Data
Right now, the service records the following information from the Davis WeatherLink API:

- Signal Quality (in %)
- Signal Strength (in dBm)
- Supercapacitor voltage (the rechargable battery that powers the VUE sensor)
- Sensor Solar Cell voltage (only VUE)
- Good Packets Streak
- Transmitter ID
- Transmitter Battery voltage (only VUE)
- Rain Bucket Tips
- Solar Radiation Sensor Solar Cell voltage
- Transmitter Battery Status (OK or LOW)
- Error Packets
- AFC (Automatic Frequency Control)
- Number of re-synchronizations
- UV Sensor Solar Cell voltage
- Console Battery voltage
- Rapid Records
- Firmware Version
- Uptime
- Touchpad Wakeups
- Bootloader Version
- Local API Queries
- Data Received (in bytes)
- Davis Health Version
- Radio Version
- EspressIF Version
- Link Uptime
- Console AC Power voltage
- Data Transmitted (in bytes)

## Installation
Install the extension:

`sudo wee_extension --install davishealthapi.zip`


## Configuration
By default, the installer installs `davishealthapi` as a service, allowing your station to keep collecting weather information via its usual driver. 
It runs during every archive interval and inserts data into its own SQL database.

Example in the weewx.conf

[davishealthapi]

    data_binding = davishealthapi_binding
    station_id = ?????
    packet_log = 0
    max_count = 13		# search for 13 sensors (8 Live, 1 indoor, 1 baro, 1 AirLink, 1 Health Live, 1 AirLink Health Record ) 
                  		#or max_count = 7 search only for 7 sensors (was the default from the origin davishealthapi)
                  		#or max_count = 0  automatical count the available sensors
    #max_ccount = 13
    max_age = None # default is 2592000
    api_key = ????????????????????????????????
    api_secret = ????????????????????????????????
    sensor_tx1 = 4
    sensor_tx2 = 1
    sensor_tx3 = 2
    sensor_tx4 = 7
    sensor_tx5 = 8
    sensor_tx6 = 0
    sensor_tx7 = 0
    sensor_tx8 = 0

Is for sensor_tx1 = 0 set, the program seach for the first found sensor and use it, 
so it's mostly better to set here the tx_ID of your VUE (or VantagePro)
If at the other (sensor_tx2, sensor_tx3 ...) 0 set, the program don't search and use such a sensor.  
If a DAVIS AirLink is also attached at the DAVIS Weatherlink Live, it's automatical used. 

### API keys
Once installed, you need to add your Davis WeatherLink Cloud API key, station ID, and secret. 
To obtain an API key and secret, go to your WeatherLink Cloud account page and look for a button marked "Generate v2 Token." 
Once you complete the process, enter your key and secret where indicated in weewx.conf.

### Station ID
Davis doesn't make it easy to make API calls, and you have to make an API call to get your station ID. 
To help the process along, I adapted one of Davis' example Python scripts to make an API call that shows your station ID. 
To use it, look for the file `davis_api_tool.py` in the zip file you downloaded. 
Open it in a text editor and type in your API key/secret where indicated. 
Save the file and run it like so:

`python3 davis_api_tool.py`

It should return 3 URLs. Open that in a browser (don't delay, the timestamp is encoded in that URL and the Davis API will reject the call 
if you wait too long to make the call) and you'll get back a string of text. Your station ID will be near the beginning. 
Enter that number into weewx.conf and you should be good to go.
    v2 API URL: Stations
    v2 API URL: Current
    v2 API URL: Historic

## Usage

Once you enable the service/driver and get it running, you won't notice anything different. 

### Own skin health
The files for this new skin (additional to the Seasons skin) are found under 
skins/health
![image](https://user-images.githubusercontent.com/93549501/145085770-f78fd1e3-a665-4138-b0c8-d63e66600e86.png)


The necessary file are there stored during the installation.
Also the stanza 

        [StdReport]
          [[DavisHealth]]
             HTML_ROOT = /var/www/html/weewx/health
             enable = true
             skin = health 

in the weeewx.conf

        [[[dayvoltSensor]]]
            data_binding = davishealthapi_binding
            title = Sensor voltages
            [[[[supercapVolt]]]]
            [[[[solarVolt]]]]
            [[[[txBattery]]]]

This should give you a result like this:
![image](https://user-images.githubusercontent.com/93549501/145085241-ac378d93-6fd3-427e-a948-9a5a27523066.png)

Note how the solar cell drops to zero as the sun goes down, the supercapacitor slowly discharges throughout the night, 
and the solar cell recharges it in the morning. If didn't get to zero so the sensor battery voltage remains untouched!

### Belchertown skin
If you're using the excellent [Belchertown skin](https://github.com/poblabs/weewx-belchertown) to display your weather data, 
you can easily add graphs to `graphs.conf` like so:

```
[[voltChart]]
        title = Voltages
        type = spline
        data_binding = davishealthapi_binding
        [[[supercapVolt]]]
        [[[solarVolt]]]
        [[[txBattery]]] 
```

This yields a graph that looks like this:
![image](https://user-images.githubusercontent.com/93549501/145085504-0a7e4f9a-634f-48d5-800c-9972d5bef002.png)


***In all cases, note that you have to specify the database binding as `davishealthapi_binding` whenever you are referencing the DavisHealthAPI data!!*** Take a look at the example files to see how that's been done so you can adapt it for your own purposes.

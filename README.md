# Weather data producer-consumer
Creates a MQTT mosquitto broker, a producer that publishes weather data for specific gps coordinates every minute and a consumer that receives the data and writes it in a csv file.

## Getting started
Create a `.env` file from the `.env.sample` containing:
- **API_KEY**: The [openweathermap](https://home.openweathermap.org/api_keys) api key.
- **LAT**: Latitude of the gps coordinates. Defaults to the current latitude.
- **LONG**: Longitude of the gps coordinates. Defaults to the current longitude.
- **FREQUENCY**: Frequency in seconds to retrieve the weather data. Defaults to 60s.
- **MOSQUITTO_USERNAME**: Broker username. Not required if authentication is disabled.
- **MOSQUITTO_PASSWORD**: Broker password. Not required if authentication is disabled.

### Authentication:

To run without authentication, set `allow_anonymous` as `true` in `config/mosquitto.conf`.

Otherwise set `allow_anonymous` as `false` and create a `config/password.txt` encrypted file containing the `username:password`. You can use the script below to autmatically create an encrypt the file:

```bash
export MOSQUITTO_USERNAME=myusername
export MOSQUITTO_PASSWORD=mypassword

echo $(docker run --rm -it eclipse-mosquitto sh -c "\
mosquitto_passwd -b -c ./mosquitto/config/password.txt $MOSQUITTO_USERNAME $MOSQUITTO_PASSWORD && \
cat ./mosquitto/config/password.txt")\
> config/password.txt
```

## Local deployment
Run the broker, producer and consumer docker containers with `docker compose up`.
The data is written in the `results/weather.csv` file.
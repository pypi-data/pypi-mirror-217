# RaspberryPi sensors

The library for getting values from sensors mh_z19, DHT, ads1015.
*Does not cause exceptions in case of errors, the cached value of sensors is also returned in case of an error*

# Examples


### start

```
from raspberry_sensors import sensors
sensors = sensors.Sensors()
```


### disabling error logging

```
sensors = sensors.Sensors(loging_error=False)
```


### get the value of DHT

```
sensors.get_dht(_type=22, gpio=4)
# _type=22 - DHT22
# _type=11 - DHT11
# gpio - GPIO pin

# return data ( dict )
# {"humidity": 36.0, "temperature": 21.0}
```


### get the value of ads

```
sensors.get_ads(chanel, interpolate=False, interpolate_min=0, interpolate_max=0)
# chanel - the channel that you want to get the voltage from
# interpolate - getting the normal value using interpolation
# interpolate_min (use if interpolate True) - minimum value at 0 V
# interpolate_max (use if interpolate True) - maximum value at 0 V

# return data ( float )
# if interpolate=False - voltage
# if interpolate=True - the voltage value to which the interpolation formula is applied 
```


### get the value of mh_z19

```
sensors.get_mhz(gpio=12, pwm=False)
# gpio - GPIO pin
# pwm - if pwm is True it will be read using pwm otherwise it is default

# return data ( dict )
# {"co2": 5000}
```
# Sentinel

This is just a fair attempt to avoid Heart Attacks from the ninja footsteps from my son, or maybe another situation when I need some focus and have my headset on with noise cancelling and my wife enters into my home office (I'm not facing the door :D). 

So [Luxafor](https://luxafor.com/) will help us here, if you wanna save some money you can do this easily with a Raspi-Zero and a led hat, [here you have more info](https://www.raspberrypi.org/blog/create-your-own-home-office-work-status-light-with-raspberry-pi/) about how to deal with that, but here we will focus us on Luxafor.

## Quickstart

- If you are running Windows or OSX, I recommend you to use the [official applications](https://luxafor.com/download/) from Luxafor, if you're a geek, you are using Linux and do you like to deal with this things, this is your place.
- Deploy the udev rules to manage Luxafor USB device, just allowing you user to write/read that device (You have a sample on `udev` folder).
    - For that just execute this commands:
    ```
    echo SUBSYSTEM=="usb", ATTR{idVendor}=="04d8", ATTR{idProduct}=="f372" MODE="0660", GROUP="$(whoami)" | sudo tee /etc/udev/rules.d/luxafor.rules
    sudo udevadm control --reload
    sudo udevadm trigger
    ```
    - Then reconnect the Luxafor device.
- Install py3 libraries using pip3
```
pip3 install -r requirements.txt
```

- Fill the variables in the script
```
HASSIO_URL = 'http://192.168.1.99:8123/api/states/'
AUTH_TOKEN = 'Bearer AAAAbbbbbBXXXBBaaa'
DEVICE_ENTITY = 'binary_sensor.lumi_lumi_sensor_magnet_ee264b02_on_off'
```

- Execute the script
```
python3 sentinel.py
```

- Try to `curl` it up from another terminal:
```
# Check The status of the door on your HomeAssistant API
curl -X GET http://192.168.1.109:8400/office_door/status

# Set an status on you Luxafor device
curl -X PUT http://192.168.1.109:8400/office_door/Opened
curl -X PUT http://192.168.1.109:8400/office_door/Closed
```


## To-Do

Remember, this is jusdt the beginning point, we will do much more.

- Systemd unit
- Better doc (some screenshots)
- Standard API for mutiple situations

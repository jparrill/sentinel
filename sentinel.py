"""
Python Script that raises up an API and changes the Luxafor's led color based on an event.

The event is managed by an external entity, in this case HomeAssistant and perform an curl
command to this API, with an URI based on the location area and the status of the sensor.
"""

import sys
import usb.core
import requests
from flask import Flask
from flask_restful import Resource, Api

class LuxaOSS(Resource):
    '''Base class for the Sentinel api'''
    def put(self, state):
        '''Set the current status on the API based on a HASSIO push (CommandLine) notification'''
        activateSentinel(dev, state)

    def get(self, state):
        '''Get Current status of the sensor (Opened/Closed)'''
        if state == 'status':
            status = recover_door_status(HASSIO_URL, AUTH_TOKEN, DEVICE_ENTITY)
        else:
            status = state

        return status

def set_color(device, color):
    '''Write color to the USB Device'''
    device.write(1, [0, colour_codes[color]])

def activateSentinel(device, state):
    '''Activate/Deactivate sentinel when the event happens'''
    try:
        ## Door Opened
        if str(state) == 'Opened':
            color = 'red'
            set_color(device, color)

        ## Door Closed
        elif str(state) == 'Closed':
            color = 'off'
            set_color(device, color)
    except Exception as e:
        print(e)

def recover_door_status(hassio_url, auth_token, device_entity):
    '''Send request to HASSIO Sensor'''
    url = hassio_url + device_entity
    headers = {
        "Content-Type": "application/json",
        "Authorization": auth_token,
    }
    status = requests.request('GET', url, headers=headers)
    json_status = status.json()
    if json_status['state'] == 'off':
        state = 'Closed'
    else:
        state = 'Opened'

    return state

def set_initial_status(device, hassio_url, auth_token, device_entity):
    ''' Set Luxafor Initial Status by checking the sensor in HASSIO '''
    status = recover_door_status(hassio_url, auth_token, device_entity)
    device.reset()
    if status == 'Opened':
        device.write(1, [0, colour_codes['red']])
    else:
        device.write(1, [0, colour_codes['off']])
    usb.util.dispose_resources(device)

# Base App
app = Flask(__name__)
app.config['TESTING'] = True
api = Api(app)
api.add_resource(LuxaOSS, '/office_door/<state>')

if __name__ == '__main__':
    # Device and Auth info
    HASSIO_URL = 'http://<your HASSIO IP>:8123/api/states/'
    AUTH_TOKEN = 'Bearer AAAAbbbbbBXXXBBaaa'
    DEVICE_ENTITY = '<Binary Sensor ID>'
    colour_codes = {'green': 71, 'yellow': 89, 'red': 82, 'blue':66, 'white': 87, 'off': 79}
    dev = usb.core.find(idVendor=0x04d8, idProduct=0xf372)

    if dev is None:
        print('Not connected')
        sys.exit()
    try:
        dev.detach_kernel_driver(0)
    except usb.core.USBError:
        pass

    set_initial_status(dev, HASSIO_URL, AUTH_TOKEN, DEVICE_ENTITY)
    app.run(debug=True, host='0.0.0.0', port=8400)

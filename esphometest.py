import aioesphomeapi
import asyncio
import websockets
import random
import datetime
import json
import planet_weight

# pip install websocket
# pip install aioesphomeapi (maybe)


def get_now():
    return datetime.datetime.now()

weight = 0
weight_date = get_now()

async def main():
    """Connect to an ESPHome device and get details."""
    loop = asyncio.get_running_loop()

    # Establish connection
    api = aioesphomeapi.APIClient(loop, "astroscale.local", 6053, "1WkzndV8oAZ5sqbe47rc")
    await api.connect(login=True)

    # Get API version of the device's firmware
    print(api.api_version)


    def change_callback(state):
        global weight
        global weight_date
        """Print the state changes of the device.."""
        print(state)
        if state is not None:
            print("state.state:", state.state)
            # if state.missing_state:
            #     weight = 0
            if state.state > 0:
                weight_date = get_now()
                weight = state.state
            else:
                time_diff = (get_now() - weight_date).total_seconds()
                if time_diff > 10:
                    weight = 0

    # Subscribe to the state changes
    await api.subscribe_states(change_callback)

async def weight_socket(websocket, path):
    global weight
    while True:
        # print(f"Sending type: {type(weight)}, weight: {weight}")
        await websocket.send(planet_weight.get_weight_json(weight))
        await asyncio.sleep(1)

start_server = websockets.serve(weight_socket, "127.0.0.1", 5678)

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(main())
    loop.run_until_complete(start_server)
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.close()






import aioesphomeapi
import asyncio
import websockets
import datetime
import time
import planet_weight
import math
import numpy as np

def get_now():
    return datetime.datetime.now()

weight_key = 520680920
weight = 0
weight_date = get_now()
planet_weight_zero = planet_weight.get_weight_json(weight)
weight_median_array = []
weight_median_array_index = -1
weight_median = 0

def update_weight_array(new_weight):
    global weight_median_array_index
    global weight_median
    global weight_median_array
    weight_median_array_index = weight_median_array_index+1
    if len(weight_median_array) < 10000:
        weight_median_array.append(new_weight)
    else:
        weight_median_array[weight_median_array_index%10000] = new_weight
    weight_median = np.median(weight_median_array)
    #print(f"Median is {weight_median}, len is {len(weight_median_array)}")

async def main():
    print("Astropolis scale starting ...")
    """Connect to an ESPHome device and get details."""
    loop = asyncio.get_running_loop()

    # Establish connection
    api = aioesphomeapi.APIClient(loop, "esp_scale_1.local", 6053, "1WkzndV8oAZ5sqbe47rc")
    await api.connect(login=True)

    # Get API version of the device's firmware
    print(api.api_version)

    # Show device details
    device_info = await api.device_info()
    print(device_info)

    # List all entities of the device
    entities = await api.list_entities_services()
    print(entities)

    def change_callback(state):
        try:
            global weight
            global weight_date
            """Print the state changes of the device.."""
            print(f"state: {state}, isWeight:{state.key == weight_key}, state isnan: {math.isnan(state.state)}")
            if state is not None and not math.isnan(state.state) and state.key == weight_key:
                weight_date = get_now()
                update_weight_array(state.state)
                weight = state.state - weight_median
                print(f"Setting weight: {weight} corrected with {weight_median} at date {weight_date}")
        except Exception as e:
            print("erroring out of callback", e)
        except:
            print("erroring out of callback 2")
    # Subscribe to the state changes
    await api.subscribe_states(change_callback)


def check_stale_weight(w, w_zero, w_date):
    time_diff = (get_now() - weight_date).total_seconds()
    if time_diff > 30:
       return w_zero
    return w

async def weight_socket(websocket, path):
    global weight
    global weight_date
    try:
        while True:
            sending = check_stale_weight(planet_weight.get_weight_json(weight, rounding=1), planet_weight_zero, weight_date)
            print(f"Sending WS: weight={weight}\n")
            await websocket.send(sending)
            await asyncio.sleep(1)
    finally:
        print("exiting weight socket")

while True:
    start_server = websockets.serve(weight_socket, "127.0.0.1", 5678)
    loop = asyncio.get_event_loop()
    try:
        # asyncio.ensure_future(main())
        loop.create_task(main())
        loop.run_until_complete(start_server)
        loop.run_forever()
    except Exception as e:
        print("catched exception", e)
    except KeyboardInterrupt:
        print("Keyb interrupt")
        pass
    finally:
        print("Closing loop.")
        loop.close()
    time.sleep(5)





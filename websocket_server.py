from aioesphomeapi import APIClient,ReconnectLogic, APIConnectionError, LogLevel
import zeroconf
import asyncio
import websockets
import datetime
import time
import planet_weight
import math
import numpy as np
import logging

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
    logging.info("Astropolis scale starting ...")
    """Connect to an ESPHome device and get details."""
    loop = asyncio.get_running_loop()

    def change_callback(state):
        try:
            global weight
            global weight_date
            """Print the state changes of the device.."""
            logging.debug(f"state: {state}, isWeight:{state.key == weight_key}, state isnan: {math.isnan(state.state)}")
            if state is not None and not math.isnan(state.state) and state.key == weight_key:
                weight_date = get_now()
                update_weight_array(state.state)
                weight = state.state - weight_median
                logging.debug(f"Setting weight: {weight} corrected with {weight_median} at date {weight_date}")
        except Exception as e:
            logging.error("erroring out of callback", e)
        except:
            logging.error("erroring out of callback 2")

    # Establish connection
    api = APIClient(loop, "esp_scale_1.local", 6053, "1WkzndV8oAZ5sqbe47rc", client_info="Moonscale")

    async def on_connect():
        try:
            await api.subscribe_states(change_callback)
            # Get API version of the device's firmware
            logging.info(api.api_version)

            # Show device details
            device_info = await api.device_info()
            logging.info(device_info)

            # List all entities of the device
            entities = await api.list_entities_services()
            logging.debug(f'Listing all entities: {entities}')
        except APIConnectionError as e:
            logging.error("Esphome api connection error", e)
            await api.disconnect()

    async def on_disconnect():
        logger.warning("Disconnected from API")

    zc = zeroconf.Zeroconf()
    reconnect = ReconnectLogic(
        client=api,
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        zeroconf_instance=zc,
    )
    await reconnect.start()
    await websockets.serve(weight_socket, "127.0.0.1", 5678, loop=loop)
    try:
        while True:
            try:
                await asyncio.sleep(5)
            except Exception as e:
                logging.error("catched exception", e)
            except KeyboardInterrupt:
                logging.error("Keyb interrupt")
                pass
    except KeyboardInterrupt:
        await reconnect.stop()
        zc.close()
    finally:
        logging.info("Closing loop.")

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
            logging.debug(f"Sending WS: weight={weight}\n")
            await websocket.send(sending)
            await asyncio.sleep(1)
    finally:
        print("exiting weight socket")

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.basicConfig(format="%(asctime)s %(name)s: %(levelname)s %(message)s")
    asyncio.run(main())



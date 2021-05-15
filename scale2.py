import pygatt
import binascii

STANDARD_SUFFIX = "-0000-1000-8000-00805f9b34fb"

def fromShortCode(code):
    return f"{code:08x}{STANDARD_SUFFIX}"

# Test in a byte if a bit is set (1) or not (0)
def isBitSet(value, bit:int) -> bool:
    return (value & (1 << bit)) != 0;

# https://www.bluetooth.com/specifications/gatt/services
SERVICE_BODY_COMPOSITION = fromShortCode(0x181b)
SERVICE_DEVICE_INFORMATION = fromShortCode(0x180a)
SERVICE_GENERIC_ACCESS = fromShortCode(0x1800)
SERVICE_GENERIC_ATTRIBUTE = fromShortCode(0x1801)
SERVICE_WEIGHT_SCALE = fromShortCode(0x181d)
SERVICE_CURRENT_TIME = fromShortCode(0x1805)
SERVICE_USER_DATA = fromShortCode(0x181C)
SERVICE_BATTERY_LEVEL = fromShortCode(0x180F)

# https://www.bluetooth.com/specifications/gatt/characteristics
CHARACTERISTIC_APPEARANCE = fromShortCode(0x2a01)
CHARACTERISTIC_BODY_COMPOSITION_MEASUREMENT = fromShortCode(0x2a9c)
CHARACTERISTIC_CURRENT_TIME = fromShortCode(0x2a2b)
CHARACTERISTIC_DEVICE_NAME = fromShortCode(0x2a00)
CHARACTERISTIC_FIRMWARE_REVISION_STRING = fromShortCode(0x2a26)
CHARACTERISTIC_HARDWARE_REVISION_STRING = fromShortCode(0x2a27)
CHARACTERISTIC_IEEE_11073_20601_REGULATORY_CERTIFICATION_DATA_LIST = fromShortCode(0x2a2a)
CHARACTERISTIC_MANUFACTURER_NAME_STRING = fromShortCode(0x2a29)
CHARACTERISTIC_MODEL_NUMBER_STRING = fromShortCode(0x2a24)
CHARACTERISTIC_PERIPHERAL_PREFERRED_CONNECTION_PARAMETERS = fromShortCode(0x2a04)
CHARACTERISTIC_PERIPHERAL_PRIVACY_FLAG = fromShortCode(0x2a02)
CHARACTERISTIC_PNP_ID = fromShortCode(0x2a50)
CHARACTERISTIC_RECONNECTION_ADDRESS = fromShortCode(0x2a03)
CHARACTERISTIC_SERIAL_NUMBER_STRING = fromShortCode(0x2a25)
CHARACTERISTIC_SERVICE_CHANGED = fromShortCode(0x2a05)
CHARACTERISTIC_SOFTWARE_REVISION_STRING = fromShortCode(0x2a28)
CHARACTERISTIC_SYSTEM_ID = fromShortCode(0x2a23)
CHARACTERISTIC_WEIGHT_MEASUREMENT = fromShortCode(0x2a9d)
CHARACTERISTIC_BATTERY_LEVEL = fromShortCode(0x2A19)
CHARACTERISTIC_CHANGE_INCREMENT = fromShortCode(0x2a99)
CHARACTERISTIC_USER_CONTROL_POINT = fromShortCode(0x2A9F)

# https://www.bluetooth.com/specifications/gatt/descriptors
DESCRIPTOR_CLIENT_CHARACTERISTIC_CONFIGURATION = fromShortCode(0x2902)
DESCRIPTOR_CHARACTERISTIC_USER_DESCRIPTION = fromShortCode(0x2901)

# extra's defined for miscale2
WEIGHT_MEASUREMENT_HISTORY_CHARACTERISTIC ="00002a2f-0000-3512-2118-0009af100700"
WEIGHT_CUSTOM_SERVICE = "00001530-0000-3512-2118-0009af100700"
WEIGHT_CUSTOM_CONFIG = "00001542-0000-3512-2118-0009af100700"

def data_handler_cb(handle, value):
    """
        Indication and notification come asynchronously, we use this function to
        handle them either one at the time as they come.
    :param handle:
    :param value:
    :return:
    """
    data = value.hex()
    measured = int((data[24:26] + data[22:24]), 16) / 200
    firstbyte_raw = data[0:2]
    firstbyte = int(firstbyte_raw, 16)
    secondbyte_raw = data[2:4]
    secondbyte = int(secondbyte_raw, 16)

    isWeightRemoved = isBitSet(secondbyte, 7)
    isDateInvalid = isBitSet(secondbyte, 6)
    isStabilized = isBitSet(secondbyte, 5)
    isLBSUnit = isBitSet(firstbyte, 0)
    isCattyUnit = isBitSet(secondbyte, 6)
    isImpedance = isBitSet(secondbyte, 1)

    print("Data: {}".format(value.hex()))
    print(f"Weight = {measured} kg")
    print(f"firstbyte: {firstbyte_raw}-{secondbyte:>08b}, secondbyte: {secondbyte_raw}-{secondbyte:>08b}")
    print(f"isWeightRemoved: {isWeightRemoved}, isStabilised: {isStabilized}")
    print("Handle: {}".format(handle))

def bluetooth(scale_mac: str):
    # The BGAPI backend will attempt to auto-discover the serial device name of the
    # attached BGAPI-compatible USB adapter.
    adapter = pygatt.backends.GATTToolBackend(search_window_size=2048)

    try:
        adapter.start()
        device = adapter.connect(scale_mac, address_type=pygatt.BLEAddressType.random, timeout=20)
        device.subscribe(CHARACTERISTIC_BODY_COMPOSITION_MEASUREMENT,
                         callback=data_handler_cb,
                         indication=True)
        input("Press enter to stop program...\n")
        # for uuid in device.discover_characteristics().keys():
        #     print("Read UUID %s: %s" % (uuid, binascii.hexlify(device.char_read(uuid))))
    finally:
        print("Stopping adapter")
        adapter.stop()


if __name__ == "__main__":
    bluetooth('F4:AD:91:94:AB:36')
    # print(fromShortCode(0x181b))4
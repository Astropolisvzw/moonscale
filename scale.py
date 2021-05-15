import blescan
import sys
import time
import bluetooth._bluetooth as bluez

dev_id = 0

sock = bluez.hci_open_dev(dev_id)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

measured_anterior = 0

def get_latest_weight():
    while True:
        try:
            returnedList = blescan.parse_events(sock, 1)
            #print(returnedList)
            if len(returnedList) > 0:
                (mac, uuid, major, minor, txpower, rssi) = returnedList[0].split(',', 6)
                # CAMBIAR LA DIRECCION MAC
                # if mac == 'f4:ad:91:94:ab:36':
                    # print(f"found mac and {uuid[0:22]}")
                    # 03021b1810161b1802a4b2

                if mac == 'f4:ad:91:94:ab:36': #and uuid[0:22] == '01880f1096ab190d161d18':
                    uuidhex = int(uuid, 16)
                    print(f"uuid: {uuid}")
                    isStabilized = True if (uuidhex & (1<<5)) != 0 else False
                    loadRemoved = True if (uuidhex & (1<<7)) != 0 else False
                    # print(f"isStabilized: {isStabilized}, loadRemoved: {loadRemoved}")
                    measunit = uuid[22:24]
                    for pos in range(1):
                         measured = int((uuid[pos+2:pos+4] + uuid[pos:pos+2]), 16) / 200
                         print(measured, measured)

                    unit = ''

                    if measunit.startswith(('03', 'b3')): unit = 'lbs'
                    if measunit.startswith(('12', 'b2')): unit = 'jin'
                    if measunit.startswith(('22', 'a2')): unit = 'Kg' ; measured = measured / 2
                    # print(f"uuid: {uuid}, measunit: {uuid[22:24]}, measured1: {uuid[26:28]}, measured1: {uuid[24:26]}, measured: {measured}, unit: {unit}")
                    print(uuid)
                    if unit:
                        if measured != measured_anterior:
                            print("measured : %s %s" % (measured, unit))
                            measured_anterior = measured
                    return measured

        except KeyboardInterrupt:
            sys.exit(1)



if __name__== "__main__":
  while True:
    get_latest_weight()
    # print(f"result is: {get_latest_weight()}")


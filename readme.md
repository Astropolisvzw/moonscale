# Usage of the esphome / hx711 / html software

## Install dependencies

```bash
sudo apt install python3 
```

```bash
pip3 install esphome aioesphomeapi numpy
```
If there are complaints about numpy, also install libatlas-base-dev


## Installing the pi zero:

- install raspbian lite
- follow https://die-antwort.eu/techblog/2017-12-setup-raspberry-pi-for-kiosk-mode/
- there's a systemd service file in the ./support dir which allows the moonscale to be started on boot, as the correct user, in the correct directory etc. Cron sucks.

## TODO

https://github.com/esphome/esphome/blob/dev/esphome/components/api/client.py

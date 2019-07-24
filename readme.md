# Usage of this Xiaomi Mi scale (v1) software

Install dependencies

```bash
sudo apt-get install bluez python-bluez python-mysqldb
```

Get the MAC address of your rpi3 or higher bluetooth device

```bash
hcitool dev
```

Scan for bluetooth devices, find the scale:

```bash
hcitool scan
```

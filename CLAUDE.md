# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Moonscale is an IoT weight display system that shows what objects would weigh on different celestial bodies. The system consists of:

1. **ESP8266 Hardware** - D1 Mini board with HX711 load cell amplifier
2. **Python Backend** - Websocket server that connects to ESP via ESPHome API
3. **Web Frontend** - Simple HTML/CSS/JS display showing Moon weight

## Architecture

### Data Flow
```
HX711 Load Cell → ESP8266 (ESPHome) → websocket_server.py → Browser (WebSocket)
```

The system uses a median-filter approach with a rolling window of 10,000 measurements to establish a baseline weight, then subtracts this from current readings to get object weight.

### Key Components

- **websocket_server.py** - Main server that:
  - Connects to ESP device via ESPHome API (aioesphomeapi)
  - Maintains median baseline using numpy (websocket_server.py:25-35)
  - Serves weight data via WebSocket on port 5678
  - Marks weights as stale after 30 seconds (websocket_server.py:107-111)

- **planet_weight.py** - Calculates weights on 23 celestial bodies using surface gravity factors. Returns JSON mapping of planet names to weights.

- **esp_scale.yaml** - ESPHome configuration for D1 Mini:
  - HX711 on pins D5 (CLK) and D6 (DOUT)
  - Linear calibration: -54400 (raw) → 0 kg, 1547573 (raw) → 65 kg
  - Updates every 1 second
  - API password authentication

- **index.html** - Web display connecting to ws://127.0.0.1:5678, displays Moon weight only

## Commands

### Development & Testing
```bash
# Run server locally
python3 websocket_server.py

# Run with random test weights
python3 websocket_server.py --random

# Enable debug logging
python3 websocket_server.py --verbose

# Test planet weight calculations
python3 planet_weight.py
```

### Production (Raspberry Pi)
```bash
# Check service status
./status.sh   # or: sudo systemctl status moonscale

# View logs
./logs.sh     # or: journalctl -u moonscale

# Restart service
./restart.sh  # or: sudo systemctl restart moonscale

# Manual start (creates timestamped log)
./start.sh
```

### ESP8266 Firmware
```bash
# Flash firmware to ESP
esphome run esp_scale.yaml

# Compile only
esphome compile esp_scale.yaml

# View logs from ESP
esphome logs esp_scale.yaml
```

## Dependencies

Install on Raspberry Pi:
```bash
pip3 install esphome aioesphomeapi numpy websockets
```

If numpy fails, also install: `sudo apt install libatlas-base-dev`

## Configuration

- **secrets.yaml** - Contains WiFi credentials and API password (gitignored)
  - `apollossid` / `apollopassword`
  - `astroiotssid` / `astroiotpassword`
  - `hackerspacessid` / `hackerspacepassword`
  - `apipassword` (for ESPHome API)

- **ESPHome connection** - Hardcoded in websocket_server.py:61:
  - Host: `esp-scale-1.local`
  - Port: `6053`
  - Uses mDNS (zeroconf) for discovery

## Weight Calibration

To recalibrate the scale, update the linear calibration values in esp_scale.yaml:28-30:
1. Get raw value with no weight → first value
2. Get raw value with known weight (e.g., 65 kg) → second value
3. Update: `- <raw_zero> -> 0` and `- <raw_known> -> <known_weight>`
4. Reflash ESP with `esphome run esp_scale.yaml`

## Systemd Service

The production deployment uses systemd (support/moonscale.service):
- Runs as user `pi`
- Working directory: `/home/pi`
- Executes start.sh on boot
- Auto-restarts on failure
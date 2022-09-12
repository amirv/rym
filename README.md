# Read Your Meter Home assistant pyscript

A pyscript to update a water meter sensor connected to Read Your Meter Pro of Arad's meters

## Installation

Install pyscript
place pyscript/apps/rym.py in /config/pyscript/apps/rym.py

Create a secret.yaml:
```
rym_email: "xxx@gmail.com"
rym_pw: "XXXXXX"
rym_deviceId: "XXXXXXXXXXXXXXXXXXXXxx"
```

Add to configuration.yaml:
```
pyscript:
  apps:
    rym:
      email: !secret rym_email
      pw: !secret rym_pw
      deviceId: !secret rym_deviceId



template:
  - sensor:
    - name: "rym"
      unit_of_measurement: "L"
      state_class: measurement
      state: 0
```

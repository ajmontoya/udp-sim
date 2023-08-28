# UDP Simulator

Simple Python and NodeJS UDP simulator that sends/receives JSON data as payload. Currently, electronic speed controller (ESC) related data is the only supported payload type. More payload types can be added in the future as needed, independent of any particular domain. The NodeJS server is not required to use the Python simulator. It is simply there to server as a mock UDP socket server for the Python script. This allows viewing the received JSON payload without standing up your own server.

> Recommended Python version is >/= 10.0 tho earlier version should work. The NodeJS is a basic, simple socket server and should be support by older Node versions.

## ESC JSON Payload

Examples of electronic speed controller data from supported Voxel drones are shown below.

The following is a constant 60% power drone test

```json
{
    "vehicle": "d126",
    "testid": 1693020077.37441,
    "testname": "test-1",
    "escid": 1,
    "params": {
        "power": 60,
        "config": 4,
        "step": null
    },
    "measurements": {
        "time": 2,
        "rpm": 3700,
        "power": 43,
        "voltage": 4.472304127218034,
        "temp": 44.74852124225166,
        "current": 0.033798149409453554
    },
    "labels": [
        "time",
        "rpm",
        "power",
        "voltage",
        "temp",
        "current"
    ],
    "uom": {
        "time": "sec",
        "rpm": "rpm",
        "power": "%",
        "voltage": "V",
        "temp": "\u00b0C",
        "current": "Amps"
    }
}
```

The following is a stepwise power drone test of 10% to 12% to 14% to 16% power level.

```json
{
    "vehicle": "d126",
    "testid": 1693020077.37441,
    "testname": "test-1",
    "escid": 1,
    "params": {
        "power": 12,
        "config": 4,
        "step": [10, 12, 14, 16]
    },
    "measurements": {
        "time": 2,
        "rpm": 3700,
        "power": 43,
        "voltage": 4.472304127218034,
        "temp": 44.74852124225166,
        "current": 0.033798149409453554
    },
    "labels": [
        "time",
        "rpm",
        "power",
        "voltage",
        "temp",
        "current"
    ],
    "uom": {
        "time": "sec",
        "rpm": "rpm",
        "power": "%",
        "voltage": "V",
        "temp": "\u00b0C",
        "current": "Amps"
    }
}
```

## vehicle value

The vehicle value is a string identifier for the drone being simulated.

## testid value

The testid value is simply just the epoch time for when the test started. In Python, this defaults to float value.

## testname

The testname value is the name/description for an individual test run.

## escid value

The escid value is the ESC number, (1 - 4).

## params object

### config

Config only accepts 4 integer values corresponding to the different drone ESC confiugrations:

- 1: Single esc
- 2: Cross axis for esc 0 & 2
- 3: Cross axis for esc 1 & 3
- 4: All 4 escs

### power

Power only accepts integer values between 0 and 100. Power is a percentage value. (In reality, the voxel drone only accepts values from 10 - 100.)

### step

Step accepts an integer list of power values that each ESC (according to the config object) will run at. So if the list

```text
10 20 30 40
```

is supplied, then each ESC will run at each of those power levels in that order.

## measurements object

The measurements object contains the value for each corresponding measurement type detailed in the labels and uom lists.

## Usage - Python script

### Help

Use the help flag to see all command line arguments and descriptions:

```python
python3 -m main --help
```

### Examples

To simulate running all 4 escs at 35% power level:

```python
python3 -m main --config 4 --power 35
```

To simulate running the 0-2 esc cross axis at 45% power level:

```python
python3 -m main --config 2 --power 45
```

To simulate with the same settings but using the name 'peterpan':

```python
python3 -m main --config 2 --power 45 --testname peterpan
```

To simulate running all 4 escs at 15% power level for 10 seconds:

```python
python3 -m main --config 4 --power 15 --timeout 10
```

> Note: The timeout flag defaults to run indefinitely. Use ctrl-c to kill the script. The UDP resources will automatically be cleaned up

To simulate running all 4 escs using a step power list of 10 - 70% in incrememnts of 10%:

```python
python3 -m main --config 4 --step 10 20 30 40 50 60 70
```

### Target IP address and port

The target socket address and port default to 127.0.0.1 and 41234, respectively. To change the address and port, simply supply the flags:

```python
python3 -m main --config 4 --power 35 -a 192.168.0.3 -p 6233
```

or the full flag descriptions can be supplied:

```python
python3 -m main --config 4 --power 35 --address 192.168.0.3 --port 6233
```

## Usage - NodeJS server socket

```javascript
node index.js
```

This will bind a socket server on 0.0.0.0 on port 41234 and print out the received JSON payloads from the Python script.

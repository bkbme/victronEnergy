# victronEnergy
Code for Victron Energy Venus OS v2.93.

Place code in /opt/victronenergy/.

## Testing
1. Make sure that your USB adapter is ignored: \
   Edit /etc/udev/rules.d/serial-starter.rules \
   Set 
   ```
   ENV{VE_SERVICE}="ignore"
   ```
2. reboot
3. Run dbus-modbus-client.py for testing.
```
root@einstein:/opt/victronenergy/dbus-modbus-client# ./dbus-modbus-client.py -h
usage: dbus-modbus-client.py [-h] [-d] [-f] [-m {ascii,rtu}] [-r RATE]
                             [-s SERIAL] [-x]

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           enable debug logging
  -f, --force-scan
  -m {ascii,rtu}, --mode {ascii,rtu}
  -r RATE, --rate RATE
  -s SERIAL, --serial SERIAL
  -x, --exit            exit on error
```

## Done with testing
1. Set /etc/udev/rules.d/serial-starter.rules back to rs485
   ```
   ENV{VE_SERVICE}="rs485"
   ```
2. reboot
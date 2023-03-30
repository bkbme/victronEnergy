# victronEnergy SDM72D-M-2 MID Modbus ESS driver
Code for Victron Energy Venus OS v2.93. / also tested on v3.00~22

The default meter password is 1000 if anyone else needs it.

Tested with the following equipment:

Counter: https://amzn.to/3LBlkum (currently only costs 51.50 EUR)

RS485 USB adapter: https://amzn.to/3Jw5lL8 (the version with FT232RL chip, currently 18.50 EUR)

So why spend so much on an ET340 that has no display?

First set your meter to 19200 baud (see manual).
Second place code in /opt/victronenergy/.

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

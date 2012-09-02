import logging
import sys

from openhome import serial_port

# Set up logger.
log = logging.getLogger('log')

# Set up handlers for both stdout and file.
stream_handler = logging.StreamHandler(sys.stdout)
log.addHandler(stream_handler)

# Set output format.
format = logging.Formatter('[%(asctime)-15s] %(levelname)7s: %(message)s')
stream_handler.setFormatter(format)

# Set logging level.
log.setLevel(logging.DEBUG)

drv = serial_port.Driver('/dev/ttyUSB0')

while(True):
    drv.read()

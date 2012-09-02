import serial
import logging

# Get logger.
log = logging.getLogger('log')


def raw2hex(raw):
    "Convert raw data to it's hexadecimal form."

    hex = ""

    # Convert each byte to it's hex value and add it to string.
    for byte in raw:
        hex += ('%02x' % ord(byte))

    return hex


def raw2desc(raw):
    "Find text description for raw data, if it's known."

    desc = {
        '\x04\x50': "Acknowledgment",
        '\x04\x56': "Set Date Request",
        '\x04\x5a': "Echo",
        '\x05\x00': "HD Status Response"
    }

    for prefix in desc.keys():
        if(raw.startswith(prefix)):
            return desc[prefix]

    return None


class Driver:
    "Class providing low-level serial port support."

    def __init__(self, device):
        "Set up and open specified serial port device (eg. /dev/ttyS0)."

        # Open specified device.
        self.port = serial.Serial(device)

        if(self.port.isOpen()):
            # Port opened, time to set it up.
            self.port.timeout = 0.05

            # Flush serial port upon opening.
            self.port.flushInput()

            log.info('Serial port device "%s" opened.' % self.port.portstr)
        else:
            log.error('Could not open serial port device"%s"'
                % self.port.portstr)
            raise Exception

    def __del__(self):
        "Close serial port correctly."

        self.port.close()

        if(not self.port.isOpen()):
            log.info('Serial port device "%s" closed' % self.port.portstr)
        else:
            log.error('Could not close serial port device "%s"'
                % self.port.portstr)

    def read(self):
        "Read raw data from serial port (non-blocking)."

        raw = self.port.read(11)

        if(raw):
            log.debug('Read "%s" (%s)' % (raw2hex(raw), raw2desc(raw)))

    def write(self, raw):
        "Write raw data to serial port."

        self.port.write(raw)

        log.debug('Written "%s"' % raw2hex(raw))

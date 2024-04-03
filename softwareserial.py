import pigpio
import logging
import time

class softwareSerial():
    def __init__(self, txd_pin, rxd_pin, baudrate, timeout=15, new="/n", eol="/n"):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        self.txd = txd_pin
        self.rxd = rxd_pin
        self.baudrate = baudrate
        self.timeout = timeout
        self.new = new
        self.eol = eol

        self.logger.info("Initializing pigpio...")
        self.pigpio = pigpio.pi()

        if not self.pigpio.connected:
            self.logger.critical("Pigpio daemon not started! Start with: `sudo pigpiod`. Exiting...")
            exit()

        self.logger.info("Initializing pins...")

        self.pigpio.set_mode(self.txd, pigpio.OUTPUT)
        self.pigpio.set_mode(self.rxd, pigpio.INPUT)

        pigpio.exceptions = False
        self.pigpio.bb_serial_read_close(self.rxd)
        
        pigpio.exceptions = True
        
        self.pigpio.bb_serial_read_open(self.rxd, self.baudrate)

    def write(self, message):
        self.logger.debug("Clearing wave...")
        self.pigpio.wave_clear()
        self.logger.debug("Creating message and connection...")
        self.pigpio.wave_add_serial(self.txd, self.baudrate, str(f"{message}\n").encode())
        self.logger.debug("Creating wave...")
        wave = self.pigpio.wave_create()
        self.logger.debug("Sending data...")
        self.pigpio.wave_send_once(wave)
        while self.pigpio.wave_tx_busy():
            pass
        self.logger.debug("Deleting wave...")
        self.pigpio.wave_delete(wave)

    def read(self):
        try:
            final_string = ""
            start = time.perf_counter()
            while round((time.perf_counter() - start), 2) < self.timeout:
                (byte_count, data) = self.pigpio.bb_serial_read(self.rxd)

                if data:
                    try:
                        data = data.decode("utf-8")
                    except AttributeError:
                        pass

                    final_string = final_string + data

                    if final_string.find(self.new) != -1:
                        while int(byte_count) > 0:
                            (byte_count, data) = self.pigpio.bb_serial_read(self.rxd)

                            try:
                                data = data.decode("utf-8")
                            except AttributeError:
                                pass

                            final_string = final_string + data

                            if final_string.find(self.eol) != -1:
                                final_string = final_string.strip(self.new)
                                final_string = final_string.strip(self.eol)
                                return final_string
            self.logger.warning("Timeout reached!")
            return None
        except Exception as e:
            self.logger.error(f"Failed to get data, error: {e}")

if __name__ == "__main__":
    serial = softwareSerial(17, 27, 9600)

    while True:
        read = serial.read()
        
        if read != None:
            if read.find("ping") != -1:
                serial.write("pong")

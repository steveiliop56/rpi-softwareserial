## Raspberry Pi Python Software Serial

A very simple raspberry pi software serial library made with python and pigpio.

### Installation

The installation is very simple you just need to have pigpio installed which can be installed with this command:

```Bash
sudo apt install python3-pigpio pigpio -y
```

After that just copy the library to your project and give the file a name (e.g. `softwareserial.py`).

### Usage

The usage is very simple you just impot it into your script set the parameters and you are ready. Here is an example:

```Python
from softwareserial import softwareSerial

serial = softwareSerial(txd_pin=17, rxd_pin=27, baudrate=9600)

serial.write("hello world!")

message = serial.read()

print(message)
```

The library uses custom new line and end of line indicators which can be changed like so:

```Python
serial = softwareSerial(txd_pin=17, rxd_pin=27, baudrate=9600, new="/n", eol="/n")
```

Furthermore you can change the read timeout like so:

```Python
serial = softwareSerial(txd_pin=17, rxd_pin=27, baudrate=9600, new="/n", eol="/n", timeout=15)
```

### License

The project is licensed under the GPL V3 License. You may modify, distribute and copy the code as long as you keep the changes in the source files. Any modifications you make using a compiler must be also licensed under the GPL license and include build and install instructions.

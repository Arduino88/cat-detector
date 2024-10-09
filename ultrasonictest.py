import pyfirmata2
import time

PORT = pyfirmata2.Arduino.AUTODETECT

# Creates a new board
board = pyfirmata2.Arduino(PORT)
print("Setting up the connection to the board ...")

# Setup the digital pin as servo
trig = board.get_pin('d:9:o')
echo = board.get_pin('d:10:i')

while True:
    trig.write(False)
    time.microsleep(2)
    trig.write(True)
    time.microsleep(10)
    trig.write(False)

    duration = 1
    
    # Wait for echo pulse
    while echo.read()!= 1:
        pass
    


# Close the serial connection to the Arduino
board.exit()
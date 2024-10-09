import serial
import time
import cat_detector as detect
import webcam_save as camera

class UltrasonicSensor:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.serial_connection = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Wait for the serial connection to initialize

    def get_distance(self):
        if self.serial_connection.in_waiting > 0:
            try:
                distance = self.serial_connection.readline().decode('utf-8').strip()
                return float(distance)
            except ValueError:
                return None
        return None

    def send_command(self, command):
        self.serial_connection.write(command.encode())

    def close(self):
        self.serial_connection.close()

    def flush(self):
        self.serial_connection.flushInput()
        self.serial_connection.flushOutput()

def scanCat() -> bool:
    camera.take_photo()
    return detect.isPittin()


if __name__ == "__main__":
    detect.init()
    camera.init()

    port = 'COM3'  # Change this to your Arduino port
    sensor = UltrasonicSensor(port)
    open = False
    lastState = open
    counter = 0
    threshhold = 40

    try:
        while True:
            lastState = open
            distance = sensor.get_distance()
            if distance is not None:
                print(f"Distance: {distance} cm")
                
                if not open: #closed
                    if distance < 20:  # If an object is closer than 20 cm
                        if scanCat():
                            open = True

                        else:
                            time.sleep(4)
                        sensor.flush()

                else: #open
                    if distance < 20:
                        open = True
                        counter = 0

                    else:
                        if counter > threshhold:
                            open = scanCat()
                            counter = 0
                        
                        else:
                            counter += 1


            print(counter)
        
            if open and not lastState:
                sensor.send_command('1')
                print('opening')
            elif not open and lastState:
                sensor.send_command('0')  # Reset the servo
                print('closing')

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        sensor.close()

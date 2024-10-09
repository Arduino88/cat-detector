import serial
import time

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

if __name__ == "__main__":
    port = 'COM3'  # Change this to your Arduino port
    sensor = UltrasonicSensor(port)
    open = False
    lastState = open
    counter = 0
    threshhold = 4

    try:
        while True:
            lastState = open
            distance = sensor.get_distance()
            if distance is not None:
                print(f"Distance: {distance} cm")
                # Example condition to send a command to the Arduino
                if distance < 20:  # If an object is closer than 10 cm
                    open = True
                    counter = 0
                    
                else:
                    if counter > threshhold:
                        open = False
                    else:
                        counter += 1
                        open = True

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

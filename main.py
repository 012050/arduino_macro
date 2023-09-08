import os
import threading

import serial

speaker = os.getcwd() + "\\BAT\\Speaker.bat"
earphone = os.getcwd() + "\\BAT\\Earphone.bat"
headset = os.getcwd() + "\\BAT\\Headset.bat"

def speaker_control():
    command = 0
    array = [0, 0, 0, 0]
    count = 0
    loop = True
    info_data = 0

    while loop:
        try:
            py_serial = serial.Serial(
                port=f'COM{info_data}',
                baudrate=9600,
            )
            while True:
                if py_serial.readable():
                    response = py_serial.readline()
                    command = str(response[:len(response)-2].decode())
                    if command == "Sound output control device connected":
                        print("Arduino connected..")
                        continue
                    if command == 'B':
                        print("스피커 출력 4")
                        os.system(speaker)
                        continue
                    elif command == 'C':
                        print("이어폰 출력 5")
                        os.system(earphone)
                        continue
                    elif command == 'D':
                        print("헤드셋 출력 6")
                        os.system(headset)
                        continue
                    if command == "7":
                        count = 0
                        array[3] = 0
                    elif count < 3:
                        count = count + 1
                    else:
                        count = 0
                    array[count] = command
                    print(f"{array}")
                    if array == ['7','8','9','#']:
                        loop = False
                        break

        except serial.SerialException as e:
            print(f"SerialException: {e}")
            info_data += 1
            if info_data > 30:
                info_data = 0

if __name__ == "__main__":
    speaker_control_thread = threading.Thread(target=speaker_control)
    speaker_control_thread.start()
    speaker_control_thread.join()
    print("End of Program")

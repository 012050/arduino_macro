import os
import threading
from tkinter import simpledialog

import serial
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import tkinter

command = 0
array = [0, 0, 0, 0]
WindowFullSize = False

try:
    path1 = os.getcwd() + "\personal_info.txt"
    f = open(path1, "r")
    info_data = f.read()
    f.close()
    s_id = info_data.split("\n")[0]
    s_pw = info_data.split("\n")[1]
except:
    root = tkinter.Tk()
    root.withdraw()
    s_id = simpledialog.askstring(title="ID", prompt="ID를 입력하세요", parent=root)
    s_pw = simpledialog.askstring(title="PW", prompt="PW를 입력하세요", show="*", parent=root)
    p_file = open("personal_info.txt", "w")
    p_file.write(s_id + "\n" + s_pw)
    p_file.close()

speaker = os.getcwd() + "\\BAT\\Speaker.bat"
earphone = os.getcwd() + "\\BAT\\Earphone.bat"
headset = os.getcwd() + "\\BAT\\Headset.bat"

def speaker_control():
    global command, array, WindowFullSize

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
                    elif command == 'A':
                        if WindowFullSize:
                            WindowFullSize = False
                        else:
                            WindowFullSize = True
                    elif command == 'B':
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
                    print(f"{array}, {WindowFullSize}")
                    if array == ['7','8','9','#']:
                        loop = False
                        break

        except serial.SerialException as e:
            print(f"SerialException: {e}")
            info_data += 1
            if info_data > 30:
                info_data = 0

def selenium_control():
    global command, array, WindowFullSize
    driver_available = False
    door = False


    while True:
        if array == ['7','8','9','#']:
            if driver_available:
                driver.close()
            print("selenium control end")
            break
        elif array == ['7','9','8','#']:
            if driver_available:
                driver.close()
                driver_available = False
            door = False
            command = 0
            array = [0, 0, 0, 0]

        if driver_available:
            if WindowFullSize:
                driver.maximize_window()
            else:
                driver.set_window_size(984, 945)
        # DOOR
        if command == "1":
            if driver_available == False:
                driver = webdriver.Chrome()
                driver.set_window_size(984, 945)
                driver_available = True

            driver.get("https://door.deu.ac.kr/sso/login.aspx")
            driver.implicitly_wait(60)
            login = driver.find_element(By.XPATH,"/html/body/form/div[2]/div[1]/div/table/tbody/tr[1]/td[2]/input")
            login.send_keys(s_id)
            pw = driver.find_element(By.CLASS_NAME,"i_text")
            pw.send_keys(s_pw,Keys.RETURN)
            driver.implicitly_wait(60)
            driver.find_element(By.XPATH,'//*[@id="gnbContent"]/div/div[2]/ol[2]/li[3]/a').click()
            driver.implicitly_wait(60)
            driver.find_element(By.ID, "btn_quick_close").click()
            driver.implicitly_wait(10)
            command = 0
            door = True

        # DAP
        elif command == "2":
            if driver_available == False:
                driver = webdriver.Chrome()
                driver.set_window_size(984, 945)
                driver_available = True
            driver.get("https://dap.deu.ac.kr/sso/login.aspx")
            driver.implicitly_wait(60)
            dap_id = driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div[1]/div[2]/input[1]")
            dap_pw = driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div[1]/div[3]/input")
            dap_id.send_keys(s_id)
            dap_pw.send_keys(s_pw, Keys.RETURN)
            driver.implicitly_wait(60)
            command = 0

        # SEARCH
        elif command == "3":
            if driver_available == False:
                driver = webdriver.Chrome()
                driver.set_window_size(984, 945)
                driver_available = True
            elif door == False:
                driver.get("https://door.deu.ac.kr/sso/login.aspx")
                driver.implicitly_wait(60)
                login = driver.find_element(By.XPATH,"/html/body/form/div[2]/div[1]/div/table/tbody/tr[1]/td[2]/input")
                login.send_keys(s_id)
                pw = driver.find_element(By.CLASS_NAME,"i_text")
                pw.send_keys(s_pw,Keys.RETURN)
            driver.get("http://door.deu.ac.kr/Community/MessageSend")
            driver.implicitly_wait(60)
            driver.find_element(By.CSS_SELECTOR, "#popsearch > span > button").click()
            command = 0

if __name__ == "__main__":
    speaker_control_thread = threading.Thread(target=speaker_control)
    selenium_control_thread = threading.Thread(target=selenium_control)

    speaker_control_thread.start()
    selenium_control_thread.start()

    speaker_control_thread.join()
    selenium_control_thread.join()
    print("End of Program")

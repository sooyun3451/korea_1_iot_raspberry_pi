import RPi.GPIO as GPIO
from threading import Thread
from time import sleep

BUTTON_PINS = [5, 6, 13]
LED_PIN = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
for BUTTON_PIN in BUTTON_PINS:
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

password = [1, 1, 1]
checkPassword = []
pass_state = False

buttonThreads = []
authenticatedStatus = "standby"

def handleLed():
    while True:
        if authenticatedStatus == "success":
            GPIO.output(LED_PIN, GPIO.HIGH)
        elif authenticatedStatus == "fail":
            GPIO.output(LED_PIN, GPIO.HIGH)
            sleep(0.2)
            GPIO.output(LED_PIN, GPIO.LOW)
            sleep(0.2)
        elif authenticatedStatus == "standby":
            GPIO.output(LED_PIN, GPIO.LOW)

def timeout():
    global checkPassword
    global authenticatedStatus
    while True:
        sleep(10)
        checkPassword = []
        authenticatedStatus = "standby"

def confirmPassword():
    global password
    global checkPassword
    global authenticatedStatus
    if password == checkPassword:
        authenticatedStatus = "success"
    else :
        authenticatedStatus = "fail"


def inputButton(BUTTON_PIN):
    while True:
        button_input = GPIO.input(BUTTON_PIN)
        if len(checkPassword) < 3 and button_input == GPIO.HIGH:
            checkPassword.append(BUTTON_PINS.index(BUTTON_PIN) + 1)
            print(checkPassword)
            if len(checkPassword) > 2:
                confirmPassword()
                checkPassword.clear()
        sleep(0.2)


if __name__ == "__main__":
    try:
        for BUTTON_PIN in BUTTON_PINS:
            inputButtonThread = Thread(target=inputButton, args=[BUTTON_PIN], daemon=True)
            buttonThreads.append(inputButtonThread)
            inputButtonThread.start()
        handleLedThread = Thread(target=handleLed, daemon=True)
        handleLedThread.start()
        timeoutThread = Thread(target=timeout, daemon=True)
        timeoutThread.start()


        while True:
            pass

    except KeyboardInterrupt:
        pass
    

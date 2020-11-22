from time import sleep, time
from machine import Pin, PWM, RTC
import micropython
import ntptime

micropython.alloc_emergency_exception_buf(100)

# Setup time via NTP
rtc = RTC()
rtc.datetime() # get date and time

ntptime.settime()
time_set_trigger = time() + 20
current_time = rtc.datetime()
print(current_time)


trigger = None
interrupt_pin = None

push_green = Pin(14, Pin.IN, Pin.PULL_UP, value=1)     # D5
push_red = Pin(5, Pin.IN, Pin.PULL_UP, value=1)       # D1
push_blue = Pin(4, Pin.IN, Pin.PULL_UP, value=1)      # D2

# led_green = Pin(15, Pin.OUT)    # D8 pin
# led_red = Pin(12, Pin.OUT)      # D6 pin
# led_blue = Pin(13, Pin.OUT)     # D7 pin

led_green = PWM(Pin(15), freq=1000)  # D8 pin
led_red = PWM(Pin(12), freq=1000)      # D6 pin
led_blue = PWM(Pin(13), freq=1000)      # D7 pin

# invert on and off if using built in led for testing
def red_interrupt(pin):
    global trigger
    trigger = "red"
    print('Red light! Pin Triggered:', pin)
    print(push_red.value())


def blue_interrupt(pin):
    global trigger
    trigger = "blue"
    print('Blue light! Pin Triggered:', pin)
    print(push_blue.value())

def green_interrupt(pin):
    global trigger
    trigger = "green"
    print('Green light! Pin Triggered:', pin)
    print(push_green.value())
    

def reset_leds():
    # led_green.off()
    # led_red.off()
    # led_blue.off()
    led_green.duty(0)
    led_red.duty(0)
    led_blue.duty(0)

def test_leds():
    led_green.duty(1023)
    sleep(1)
    reset_leds()

    led_red.duty(1023)
    sleep(1)
    reset_leds()

    led_blue.duty(1023)
    sleep(1)
    reset_leds()
    

reset_leds()
test_leds()

push_red.irq(trigger=Pin.IRQ_FALLING, handler=red_interrupt)
push_blue.irq(trigger=Pin.IRQ_FALLING, handler=blue_interrupt)
push_green.irq(trigger=Pin.IRQ_FALLING, handler=green_interrupt)

while True:
    timeout = time() + 10*3 # 10 seconds
    if trigger:
        print("Trigger detected.")
        print(trigger)
        if trigger == "red":
            led_red.duty(1023)
            while trigger == "red" and time() < timeout:
                sleep(1)
            print("Resetting trigger")
            trigger = None
            reset_leds()
        elif trigger == "blue":
            led_blue.duty(1023)
            while trigger == "blue" and time() < timeout:
                sleep(1)
            print("Resetting trigger")
            trigger = None
            reset_leds()
        elif trigger == "green":
            led_green.duty(1023)
            while trigger == "green" and time() < timeout:
                sleep(1)
            print("Resetting trigger")
            trigger = None
            reset_leds()

    sleep(0.5)

    try:
        if time() > time_set_trigger:
            print("Syncing time...")
            ntptime.settime()
            time_set_trigger = time() + 7200
            print(rtc.datetime())
            print("Time (UTC): {0}:{1}".format(rtc.datetime()[4], rtc.datetime()[5]))
    except:
        pass

    # led_green.on()
    # sleep(0.5)
    # led_green.off()

    # led_red.on()
    # sleep(0.5)
    # led_red.off()

    # led_blue.on()
    # sleep(0.5)
    # led_blue.off()


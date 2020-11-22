# boot.py - - runs on boot-up
from time import sleep, time

def do_connect():
    import network

    timeout = time() + 10 # 10 seconds

    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('MonkeyBalls', '10241024bb')
        while not sta_if.isconnected() and time() < timeout:
            pass

    print('network config:', sta_if.ifconfig())

do_connect()

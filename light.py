#!/usr/bin/python3

"""
    Program:        Remote LED (light.py)
    Author:         M. Heidenreich, (c) 2021
    Description:    This code is provided in support of the following YouTube tutorial:
                    https://youtu.be/D-4kx98c_aE

    This tutorial demonstrates how to use pigpiod daemon with Python gpiozero
    to operate electronic components remotely with Raspberry Pi.

    THIS SOFTWARE AND LINKED VIDEO TOTORIAL ARE PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS
    ALL WARRANTIES INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
    IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES
    OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
    NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from gpiozero import PWMLED, Button, MCP3002
from gpiozero.pins.pigpio import PiGPIOFactory
from signal import pause

remote_host = PiGPIOFactory(host="raspberrypi3.local")
adc = MCP3002(0)

light = PWMLED(26, pin_factory=remote_host)
button = Button(21)

def compensated_values():
    for value in adc.values:
        yield pow(2, value/0.10035)/1000

def toggle_light():
    if light.source:
        light.source = None
        light.off()
    else:
        light.source = compensated_values()

try:
    button.when_pressed = toggle_light 
    
    light.source_delay = 0.02

    pause()

except KeyboardInterrupt:
    pass

finally:
    light.close()

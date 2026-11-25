# ESP32 Smart Lighting Controller

A beginner-friendly ESP32 project that switches a low-voltage LED load using a relay module and a push button.

## Scope and safety
This example is designed for a low-voltage DC LED load only. Do not connect household mains voltage. If mains switching is required, use a properly rated enclosed product and a qualified electrician.

## Hardware
- ESP32 development board.
- 3.3V-compatible relay module (verify the exact module input requirements).
- Momentary push button.
- Low-voltage LED strip or lamp with a suitable DC power supply.
- Jumper wires and breadboard for the control circuit.

## Pin map
- Relay IN → GPIO 26.
- Button → GPIO 27 and GND (internal pull-up enabled).
- Relay VCC/GND → according to the relay module's documented requirements.
- LED load → relay contacts and a separate correctly rated low-voltage supply.

## Behavior
Pressing the button toggles the light state. A short debounce interval prevents multiple toggles from one press.

## Build
Open `smart_lighting.ino` in Arduino IDE, select the correct ESP32 board and port, verify the relay's active HIGH/LOW behavior, then upload.

## Before powering
Check board pinout, relay logic level, supply polarity, LED current, and common-ground requirements from the component datasheets. Never power the LED load from an ESP32 GPIO.

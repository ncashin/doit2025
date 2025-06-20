#!/usr/bin/env python3
"""
Wii Remote Input Reader using libcwiid

This script connects to a Wii remote via Bluetooth and reads various inputs:
- Button presses
- Accelerometer data
- IR sensor data
- Battery level

Requirements:
- libcwiid library (install with: pip install cwiid)
- Bluetooth enabled system
- Wii remote in discoverable mode

Usage:
    python wii_remote_reader.py
"""

import cwiid
import time
import sys
from threading import Thread

class WiiRemoteReader:
    def __init__(self):
        self.wiimote = None
        self.connected = False
        self.running = False
        
    def connect(self):
        """Connect to Wii remote"""
        print("Press 1+2 on your Wii remote to connect...")
        try:
            self.wiimote = cwiid.Wiimote()
            self.connected = True
            print("Connected to Wii remote!")
            
            # Enable button and accelerometer reporting
            self.wiimote.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_IR
            self.wiimote.led = cwiid.LED1_ON
            
            # Set up rumble to indicate connection
            self.wiimote.rumble = 1
            time.sleep(0.5)
            self.wiimote.rumble = 0
            
        except RuntimeError as e:
            print(f"Failed to connect: {e}")
            print("Make sure your Wii remote is in discoverable mode (press 1+2)")
            return False
        return True
    
    def disconnect(self):
        """Disconnect from Wii remote"""
        if self.wiimote:
            self.wiimote.close()
            self.connected = False
            print("Disconnected from Wii remote")
    
    def get_button_name(self, button):
        """Convert button code to readable name"""
        buttons = {
            cwiid.BTN_1: '1',
            cwiid.BTN_2: '2',
            cwiid.BTN_A: 'A',
            cwiid.BTN_B: 'B',
            cwiid.BTN_PLUS: 'PLUS',
            cwiid.BTN_MINUS: 'MINUS',
            cwiid.BTN_HOME: 'HOME',
            cwiid.BTN_LEFT: 'LEFT',
            cwiid.BTN_RIGHT: 'RIGHT',
            cwiid.BTN_UP: 'UP',
            cwiid.BTN_DOWN: 'DOWN'
        }
        return buttons.get(button, f'UNKNOWN({button})')
    
    def format_accelerometer(self, acc):
        """Format accelerometer data"""
        x, y, z = acc
        return f"X: {x:3d}, Y: {y:3d}, Z: {z:3d}"
    
    def format_ir(self, ir):
        """Format IR sensor data"""
        if not ir:
            return "No IR sources detected"
        
        ir_data = []
        for i, source in enumerate(ir):
            if source:
                x, y, size = source
                ir_data.append(f"Source{i+1}: ({x:3d}, {y:3d}) size:{size:3d}")
        
        return " | ".join(ir_data) if ir_data else "No IR sources detected"
    
    def get_battery_level(self):
        """Get battery level as percentage"""
        if self.wiimote:
            return self.wiimote.state['battery'] * 100
        return 0
    
    def read_inputs(self):
        """Main loop for reading Wii remote inputs"""
        print("\n=== Wii Remote Input Reader ===")
        print("Press Ctrl+C to exit")
        print("=" * 30)
        
        self.running = True
        
        while self.running and self.connected:
            try:
                # Read state
                state = self.wiimote.state
                
                # Clear screen (works on most terminals)
                print("\033[2J\033[H", end="")
                
                print("=== Wii Remote Input Reader ===")
                print(f"Battery: {self.get_battery_level():.1f}%")
                print("=" * 30)
                
                # Buttons
                buttons = state['buttons']
                if buttons:
                    pressed_buttons = []
                    for button_code in [cwiid.BTN_1, cwiid.BTN_2, cwiid.BTN_A, cwiid.BTN_B,
                                       cwiid.BTN_PLUS, cwiid.BTN_MINUS, cwiid.BTN_HOME,
                                       cwiid.BTN_LEFT, cwiid.BTN_RIGHT, cwiid.BTN_UP, cwiid.BTN_DOWN]:
                        if buttons & button_code:
                            pressed_buttons.append(self.get_button_name(button_code))
                    
                    print(f"Buttons: {', '.join(pressed_buttons)}" if pressed_buttons else "Buttons: None")
                else:
                    print("Buttons: None")
                
                # Accelerometer
                acc = state['acc']
                print(f"Accelerometer: {self.format_accelerometer(acc)}")
                
                # IR Sensor
                ir = state['ir_src']
                print(f"IR Sensor: {self.format_ir(ir)}")
                
                # Raw button state (for debugging)
                print(f"Raw Button State: {bin(buttons)}")
                
                print("\nPress Ctrl+C to exit")
                
                time.sleep(0.1)  # Update 10 times per second
                
            except KeyboardInterrupt:
                print("\nExiting...")
                self.running = False
                break
            except Exception as e:
                print(f"Error reading input: {e}")
                break
    
    def start(self):
        """Start the Wii remote reader"""
        if self.connect():
            try:
                self.read_inputs()
            finally:
                self.disconnect()
        else:
            print("Could not connect to Wii remote")

def main():
    """Main function"""
    print("Wii Remote Input Reader")
    print("Make sure your Wii remote is in discoverable mode")
    print("(Press and hold the 1 and 2 buttons simultaneously)")
    
    reader = WiiRemoteReader()
    reader.start()

if __name__ == "__main__":
    main() 
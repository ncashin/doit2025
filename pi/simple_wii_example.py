#!/usr/bin/env python3
"""
Simple Wii Remote Example

A basic example showing how to connect to and read button presses from a Wii remote.
"""

import cwiid
import time

def main():
    print("Simple Wii Remote Example")
    print("Press 1+2 on your Wii remote to connect...")
    
    try:
        # Connect to Wii remote
        wiimote = cwiid.Wiimote()
        print("Connected!")
        
        # Enable button reporting
        wiimote.rpt_mode = cwiid.RPT_BTN
        
        # Turn on LED to show connection
        wiimote.led = cwiid.LED1_ON
        
        # Rumble to confirm connection
        wiimote.rumble = 1
        time.sleep(0.5)
        wiimote.rumble = 0
        
        print("Press buttons on your Wii remote (Ctrl+C to exit)")
        
        while True:
            # Read button state
            buttons = wiimote.state['buttons']
            
            # Check for specific buttons
            if buttons & cwiid.BTN_A:
                print("A button pressed!")
            if buttons & cwiid.BTN_B:
                print("B button pressed!")
            if buttons & cwiid.BTN_1:
                print("1 button pressed!")
            if buttons & cwiid.BTN_2:
                print("2 button pressed!")
            if buttons & cwiid.BTN_HOME:
                print("HOME button pressed!")
                break  # Exit on HOME button
            
            time.sleep(0.1)
            
    except RuntimeError:
        print("Failed to connect. Make sure your Wii remote is in discoverable mode.")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        if 'wiimote' in locals():
            wiimote.close()

if __name__ == "__main__":
    main() 
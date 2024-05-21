#*********************************** ORIGINAL TOF DF Robot PYTHON CODE ******************************

#import smbus
#import time
#
#address = 0x74
#bus = smbus.SMBus(3)  # I2C bus number may vary (0 or 1) depending on your system
#
#def read_reg(reg, size):
#    try:
#        data = bus.read_i2c_block_data(address, reg, size)
#        return data
#    except IOError:
#        print("Error reading data. Check your I2C connection.")
#        return None
#
#def write_reg(reg, data):
#    try:
#        bus.write_i2c_block_data(address, reg, data)
#        return True
#    except IOError:
#        print("Error writing data. Check your I2C connection.")
#        return False
#
#def main():
#    dat = 0xB0
#    distance = 0
#
#    while True:
#        write_reg(0x10, [dat])
#        time.sleep(0.03)
#        buf = read_reg(0x02, 2)
#        
#        if buf:
#            distance = (buf[0] << 8) + buf[1] + 10
#            print(f"distance={distance}mm")
#        
#        time.sleep(0.1)

#if __name__ == "__main__":
#    main()


#******************** VERSION - 1 TOF 4 METER DFRobot WALK CODE *********************
  
import time
import sys
import vlc
import gpio as GPIO
#import smbus
from smbus2 import SMBus
from pydub import AudioSegment
sys.path.insert(0, '/home/rock/Desktop/Hearsight/')
from play_audio import GTTSA

play_audio = GTTSA()
GPIO.setup(448, GPIO.IN)  # Exit Button
bus = SMBus(3)
#bus = smbus.SMBus(3)
time.sleep(1)
addr = 0x74

def read_reg(reg, size):
    try:
        data = bus.read_i2c_block_data(addr, reg, size)
        return data
    except IOError:
        return None

def write_reg(reg, data):
    try:
        bus.write_i2c_block_data(addr, reg, data)
        return True
    except IOError:
        return False

def main():
    dat = 0xB0
    distance = 0
    meter_to_feet = 3.28084  # Conversion factor from meters to feet

    while True:
        write_reg(0x10, [dat])
        time.sleep(0.03)
        buf = read_reg(0x02, 2)
        
        if buf:
            distance_mm = (buf[0] << 8) + buf[1] + 10
            distance_m = distance_mm / 1000.0  # Convert mm to meters
#            print(f"distance={distance_m}m")
            distance_ft = distance_m * meter_to_feet  # Convert meters to feet
            print(f"Distance = {distance_ft} feet")
#            print(f"distance={distance_ft}ft")
#            print ("  Distance : %.1f ft" % distance_ft)
            print("Distance:", round(distance_ft))
            
#            if 1.524 <= distance_m <= 2.1336: #5 to 7 feet
            if 5 <= distance_ft <= 7:  # 5 to 7 feet
                media = vlc.MediaPlayer("/home/rock/Desktop/Hearsight/audios/beeb/340Hz-5sec.wav")
                media.play()
                time.sleep(1.25)
                media.stop()
                print("ALERT!!!")
                
#            elif 0.9144 <= distance_m <= 1.2192: #3 to 4 feet
            elif 3 <= distance_ft <= 4:  # 3 to 4 feet
                media = vlc.MediaPlayer("/home/rock/Desktop/Hearsight/audios/beeb/3_long_high.mp3")
                media.play()
                time.sleep(1.25)
                media.stop()
                print("STOP!!!")

            input_state = GPIO.input(448)
            if input_state:
                bus.close()
                play_audio.play_machine_audio("feature_exited.mp3")
                sys.exit()
                break
            
        time.sleep(0.1)

if __name__ == "__main__":
    main()


#******************** VERSION - 2 TOF 4 METER DFRobot WALK CODE *********************
    
import time
import sys
import vlc
import gpio as GPIO
import subprocess
#import smbus
from smbus2 import SMBus
from pydub import AudioSegment
sys.path.insert(0, '/home/rock/Desktop/Hearsight/')
from play_audio import GTTSA

play_audio = GTTSA()
GPIO.setup(448, GPIO.IN)  # Exit Button
bus = SMBus(3)
#bus = smbus.SMBus(3)
time.sleep(1)
addr = 0x74

def read_reg(reg, size):
    try:
        data = bus.read_i2c_block_data(addr, reg, size)
        return data
    except IOError:
        return None

def write_reg(reg, data):
    try:
        bus.write_i2c_block_data(addr, reg, data)
        return True
    except IOError:
        return False

def main():
    dat = 0xB0
    distance = 0
    meter_to_feet = 3.28084  # Conversion factor from meters to feet
    
    try:
        while True:
            write_reg(0x10, [dat])
            time.sleep(0.03)
            buf = read_reg(0x02, 2)
            
            if buf:
                distance_mm = (buf[0] << 8) + buf[1] + 10
                distance_m = distance_mm / 1000.0  # Convert mm to meters
#                    print(f"distance={distance_m}m")
                distance_ft = distance_m * meter_to_feet  # Convert meters to feet
                print(f"Distance = {distance_ft} feet")
#                    print ("  Distance : %.1f ft" % distance_ft)
#                    print("Distance:", round(distance_ft))
                
#                    if 1.524 <= distance_m <= 2.1336: #5 to 7 feet
                if 5 <= distance_ft <= 7:  # 5 to 7 feet
                    media = vlc.MediaPlayer("/home/rock/Desktop/Hearsight/audios/beeb/340Hz-5sec.wav")
                    media.play()
                    time.sleep(1.25)
                    media.stop()
                    print("ALERT!!!")
                    
#                    elif 0.9144 <= distance_m <= 1.2192: #3 to 4 feet
                elif 3 <= distance_ft <= 4:  # 3 to 4 feet
                    media = vlc.MediaPlayer("/home/rock/Desktop/Hearsight/audios/beeb/3_long_high.mp3")
                    media.play()
                    time.sleep(1.25)
                    media.stop()
                    print("STOP!!!")

                input_state = GPIO.input(448)
                if input_state:
                    bus.close()
                    play_audio.play_machine_audio("feature_exited.mp3")
                    sys.exit()
                    break
                
            time.sleep(0.1)
                
    except Exception as e:
        print(f"Error occurred: {e}")
        play_audio.play_machine_audio("hold_on_connection_in_progress_initiating_shortly.mp3")
        play_audio.play_machine_audio("Thank You.mp3")
        subprocess.run(["reboot"])

if __name__ == "__main__":
    main()
    

#******************** VERSION - 3 DF Robot TOF 4 METER DFRobot WALK & GOSEE CODE *********************
    
#******************************** VERSION - 3 DF Robot TOF WALK CODE *******************************
    
import time
import sys
import vlc
import gpio as GPIO
import subprocess
#import smbus
from smbus2 import SMBus
from pydub import AudioSegment
sys.path.insert(0, '/home/rock/Desktop/Hearsight/')
from play_audio import GTTSA

play_audio = GTTSA()
GPIO.setup(448, GPIO.IN)  # Exit Button
bus = SMBus(3)
#bus = smbus.SMBus(3)
time.sleep(1)
addr = 0x74

def read_reg(reg, size):
    try:
        data = bus.read_i2c_block_data(addr, reg, size)
        return data
    except IOError:
        return None

def write_reg(reg, data):
    try:
        bus.write_i2c_block_data(addr, reg, data)
        return True
    except IOError:
        return False

def main():
    dat = 0xB0
    distance = 0
    meter_to_feet = 3.28084  # Conversion factor from meters to feet
    
    try:
        while True:
            write_reg(0x10, [dat])
            time.sleep(0.03)
            buf = read_reg(0x02, 2)
            
            if buf:
                distance_mm = (buf[0] << 8) + buf[1] + 10
                distance_m = distance_mm / 1000.0  # Convert mm to meters
#                print(f"distance={distance_m}m")
                distance_ft = distance_m * meter_to_feet  # Convert meters to feet
                print(f"Distance = {distance_ft} Feet")
#                print ("  Distance : %.1f ft" % distance_ft)
#                distance_ft = round(distance_ft)
#                print("Distance in Feet:", distance_ft)
#                print("Distance:", round(distance_ft))
                
#                if 1.524 <= distance_m <= 2.1336: #5 to 7 feet
                if 5 <= distance_ft <= 7:  # 5 to 7 feet
                    media = vlc.MediaPlayer("/home/rock/Desktop/Hearsight/audios/beeb/340Hz-5sec.wav")
                    media.play()
                    time.sleep(1.25)
                    media.stop()
                    print("ALERT!!!")
                    
#                elif 0.9144 <= distance_m <= 1.2192: #3 to 4 feet
                elif 3 <= distance_ft <= 4:  # 3 to 4 feet
                    media = vlc.MediaPlayer("/home/rock/Desktop/Hearsight/audios/beeb/3_long_high.mp3")
                    media.play()
                    time.sleep(1.25)
                    media.stop()
                    print("STOP!!!")

                input_state = GPIO.input(448)
                if input_state:
                    bus.close()
                    play_audio.play_machine_audio("feature_exited.mp3")
                    sys.exit()
                    break
                
            time.sleep(0.1)
                
    except Exception as e:
        print(f"Error occurred: {e}")
        play_audio.play_machine_audio("hold_on_connection_in_progress_initiating_shortly.mp3")
        play_audio.play_machine_audio("Thank You.mp3")
        subprocess.run(["reboot"])

if __name__ == "__main__":
    main()
    
    
    
#******************************** VERSION - 3 DF Robot TOF GOSEE CODE *******************************
    
import time
import sys
import vlc
import gpio as GPIO
import subprocess
from smbus2 import SMBus
from pydub import AudioSegment
sys.path.insert(0, '/home/rock/Desktop/Hearsight/')
from play_audio import GTTSA
from English.go_see.what import SSD

what_obj = SSD()
play_audio = GTTSA()
GPIO.setup(448, GPIO.IN)  # Exit Button
bus = SMBus(3)
time.sleep(1)
addr = 0x74

def read_reg(reg, size):
    try:
        data = bus.read_i2c_block_data(addr, reg, size)
        return data
    except IOError:
        return None

def write_reg(reg, data):
    try:
        bus.write_i2c_block_data(addr, reg, data)
        return True
    except IOError:
        return False

def main():
    dat = 0xB0
    distance = 0
    meter_to_feet = 3.28084  # Conversion factor from meters to feet
    try:
        while True:
            write_reg(0x10, [dat])
            time.sleep(0.03)
            buf = read_reg(0x02, 2)
            
            if buf:
                distance_mm = (buf[0] << 8) + buf[1] + 10
                distance_m = distance_mm / 1000.0  # Convert mm to meters
#                print(f"distance={distance_m}m")
                distance_ft = distance_m * meter_to_feet  # Convert meters to feet
                print(f"Distance = {distance_ft} Feet")
#                print ("  Distance : %.1f ft" % distance_ft)
#                distance_ft = round(distance_ft)
#                print("Distance in Feet:", distance_ft)
#                print("Distance:", round(distance_ft))
                
#                if 1.524 <= distance_m <= 2.1336: #5 to 7 feet
                if 5 <= distance_ft <= 7:  # 5 to 7 feet
                    media = vlc.MediaPlayer("/home/rock/Desktop/Hearsight/audios/beeb/340Hz-5sec.wav")
                    media.play()
                    time.sleep(1.25)
                    media.stop()
                    print("ALERT!!!")
                    what_obj.detect()
                    
#                elif 0.9144 <= distance_m <= 1.2192: #3 to 4 feet
                elif 3 <= distance_ft <= 4:  # 3 to 4 feet
                    media = vlc.MediaPlayer("/home/rock/Desktop/Hearsight/audios/beeb/3_long_high.mp3")
                    media.play()
                    time.sleep(1.25)
                    media.stop()
                    print("STOP!!!")
                    what_obj.detect()

                input_state = GPIO.input(448)
                if input_state:
                    bus.close()
                    play_audio.play_machine_audio("feature_exited.mp3")
                    sys.exit()
                    break
                
            time.sleep(0.1)
            
    except Exception as e:
        print(f"Error occurred: {e}")
        play_audio.play_machine_audio("hold_on_connection_in_progress_initiating_shortly.mp3")
        play_audio.play_machine_audio("Thank You.mp3")
        subprocess.run(["reboot"])

if __name__ == "__main__":
    main()

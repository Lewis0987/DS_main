import os
import time

#跑馬燈輪播
def print_marquee(message, width=20, speed=1):
    message = '12345' + message + '67890'  # Add spaces to the message for smoother scrolling

    while True:
        for a in range(len(message) - width + 21):
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear console screen

            # ANSI escape codes for yellow background and red font color
            formatted_message = f"\033[43;31m{message[a:a+width]}\033[0m"
            
            print(formatted_message)
            time.sleep(speed)



#輪播次數
counter = 0
while True:
    print("This is an infinite loop!")

    counter += 1
    if counter >= 3:
        break  # Break out of the loop after 10 iterations
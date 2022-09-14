from tkinter import *
from tkinter.filedialog import askopenfilename,asksaveasfilename
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy.io.wavfile import read
from time import sleep
import speech_recognition as sr
import wave
import RPi.GPIO as GPIO
import math
import subprocess

def clear():
    exit()

#A function used to calculate the average distance between the frequency waves
def distance():
    input_data = read(r"/home/pi/speech2.wav")
    password_data = read(r"/home/pi/speech.wav")
    audio2 = password_data[1]
    audio = input_data[1]
    
    avg_input = (sum(audio) / len(audio))

    # if statement to decide if the input is close enough to the avg password data
    print("avg "+str(avg))
    print("avg input "+str(avg_input))
    if (avg_input >= avg - 1) and (avg_input <= avg + 1):
        print(avg_input)
        print(avg)
        return True
    else:
        return False
    

#graph for different frequencies         
def plot():
    fig = Figure(figsize = (10,10), dpi = 65)
    
    password_data = read(r"/home/pi/speech.wav")
    input_data = read(r"/home/pi/speech2.wav")
    input1 = input_data[1]
    
    password = password_data[1]

    plot1 = fig.add_subplot(211)
    plot1.set_title("Password Data")
    plot1.plot(password)
    

    plot2 = fig.add_subplot(212)
    plot2.plot(input1)
    plot2.set_title("Input Data")
    
    canvas = FigureCanvasTkAgg(fig, master = window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    


button = 25
running = True
denied = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

window = Tk()
window.geometry("800x800")
clear_button = Button(master = window, text = "Clear", command = lambda : clear())
clear_button.pack()

a = sr.Recognizer()

avgL=[]

#A loop that prompts the user to record a password
for i in range (0,3):
    with sr.Microphone() as source:
        #a.adjust_for_ambient_noise(source)
        print("Record a password...")
        audio = a.listen(source, timeout=5)

        # new addition to save the recording
        with open(r"/home/pi/speech.wav", 'wb') as f:
            f.write(audio.get_wav_data())

            temp = read(r"/home/pi/speech.wav")
            avgL.append(sum(temp[1]) / len(temp[1]))
            data=a.recognize_google(audio)
            print("password saved.")
            #print(data)

print(avgL)
avg = (sum(avgL) / len(avgL))
print(avg)

#main program loop
while running:
    if (GPIO.input(button) == GPIO.HIGH):
        with sr.Microphone() as source:
            b = sr.Recognizer()
            #b.adjust_for_ambient_noise(source)
            print("Say something...")
            audio2 = b.listen(source, timeout=5)
            
            # new addition to save the recording
            with open(r"/home/pi/speech2.wav", 'wb') as d:
                d.write(audio2.get_wav_data())
                
            data2=b.recognize_google(audio2)
            with open(r"/home/pi/speech2.wav", 'wb') as d:
                d.write(audio2.get_wav_data())
                
            data2=b.recognize_google(audio2)

            if(data2 == data):
                #print("password: {}".format(data))
                print("password attempt: {}".format(data2))
                plot()

                if (distance() == True):
                    # unlock the file or whatever
                    print("ACCESS GRANTED")
                    subprocess.call(["xdg-open", '/home/pi'])
                    break
                else:
                    print("ACCESS DENIED")

            else:
                print("wrong password try again")


                
    elif(GPIO.input(button) == GPIO.LOW):
        print("Push the button to record audio...")
        
        while(GPIO.input(button) == GPIO.LOW):
            sleep(0.1)
        if(GPIO.input(button) == GPIO.HIGH):
            continue


window.mainloop()

import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
from easygui import *
import os
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
import string

from PIL import Image
img = Image.open("signlang.png")
img = img.resize((500, 300), Image.LANCZOS)
img.save("signlang_resized.png")



# Class to display and animate GIFs in Tkinter
class ImageLabel(tk.Label):
    """A label that displays images, and plays them if they are GIFs."""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

# Function to recognize speech and display corresponding sign language GIFs or letters
def func():
    r = sr.Recognizer()
    
    # List of predefined words with corresponding sign language GIFs
    isl_gif = [
        'all the best', 'any questions', 'are you angry', 'are you busy', 'are you hungry',
        'are you sick', 'be careful', 'can we meet tomorrow', 'did you book tickets',
        'did you finish homework', 'do you go to office', 'do you have money',
        'do you want something to drink', 'do you want tea or coffee', 'do you watch TV',
        'dont worry', 'flower is beautiful', 'good afternoon', 'good evening', 'good morning',
        'good night', 'good question', 'had your lunch', 'happy journey', 'hello what is your name',
        'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing',
        'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything',
        'i go to a theatre', 'i love to shop', 'i had to say something but i forgot',
        'i have headache', 'i like pink colour', 'i live in nagpur', 'lets go for lunch',
        'my mother is a homemaker', 'my name is john', 'nice to meet you', 'no smoking please',
        'open the door', 'please call an ambulance', 'please call me later', 'please clean the room',
        'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime',
        'shall I help you', 'shall we go together tomorrow', 'sign language interpreter', 'sit down',
        'stand up', 'take care', 'there was traffic jam', 'wait I am thinking', 'what are you doing',
        'what is the problem', 'what is todays date', 'what is your age', 'what is your father do',
        'what is your job', 'what is your mobile number', 'what is your name', 'whats up',
        'when is your interview', 'when we will go', 'where do you stay', 'where is the bathroom',
        'where is the police station', 'you are wrong'
    ]

    # List of letters for individual letter recognition
    arr = list(string.ascii_lowercase)

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # Adjust for background noise
        
        while True:
            print("Say something...")
            audio = r.listen(source)  # Capture audio

            try:
                # Recognize speech using Google Speech Recognition
                a = r.recognize_google(audio).lower()
                print("You said:", a)

                # Remove punctuation
                for c in string.punctuation:
                    a = a.replace(c, "")

                # Exit if user says 'goodbye'
                if a == 'goodbye':
                    print("Oops! Time to say goodbye")
                    break
                
                # Show GIF if phrase matched
                elif a in isl_gif:
                    gif_filename = f"{a}.gif"  
                    
                    # Construct full path to the GIF file
                    gif_path = os.path.join(
                        r"C:\Users\nidhi\OneDrive\Desktop\Audio-To-Sign-Language-Translator-master\ISL_Gifs",
                        gif_filename
                    )
                    
                    if os.path.isfile(gif_path):
                        root = tk.Tk()
                        root.title(a)  # Optional: title the window with phrase
                        
                        lbl = ImageLabel(root)
                        lbl.pack()
                        lbl.load(gif_path)
                        
                        root.mainloop()
                    else:
                        print(f"GIF file not found: {gif_path}")
                
                # Show each letter image if input is not in list of phrases
                else:
                    for char in a:
                        if char in arr:
                            image_path = f'letters/{char}.jpg'  
                            if os.path.isfile(image_path):
                                image = Image.open(image_path)
                                plt.imshow(np.asarray(image))
                                plt.axis('off')
                                plt.draw()
                                plt.pause(0.8)  
                                plt.clf()
                            else:
                                print(f"Letter image not found: {image_path}")
                        else:
                            continue

            except sr.UnknownValueError:
                print("Could not understand the audio")
            except sr.RequestError:
                print("Error connecting to the recognition service")
            except Exception as e:
                print("Error:", str(e))

        plt.close()

# Main GUI interaction
while True:
    image = "signlang.png"  
    msg = "HEARING IMPAIRMENT ASSISTANT"
    choices = ["Live Voice", "All Done!", " "]
    reply = buttonbox(msg, image=image, choices=choices)

    if reply == choices[0]:
        func()
    elif reply == choices[1]:
        quit()
    elif reply == choices[2]:
        os.system("selecting.py")

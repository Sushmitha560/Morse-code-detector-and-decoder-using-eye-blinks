import cv2 as cv
from tkinter import *
from PIL import Image, ImageTk
from opencam import Camera
from openvideo import Video
import matplotlib.pyplot as plt
# Import the required module for text 
# to speech conversion
import gtts
from playsound import playsound

  
# This module is imported so that we can 
# play the converted audio
import os

class Main_Win:
    def __init__(self,root):
        self.root = root
        self.root.title("Morse code detector and decoder using eye blinks")
        self.root.geometry("1000x600+10+10")

        img = Image.open(r"C:\Users\Lenovo\OneDrive\Pictures\dark1.jpg")
        img = img.resize((1000,600),Image.ANTIALIAS)
        self.photoimg = ImageTk.PhotoImage(img)
        lblimg = Label(self.root, image=self.photoimg, bd = 4,relief = RIDGE )
        lblimg.place(x=0, y=0,width=1000,height=600)

        l = Label(self.root, text = "MORSE CODE DETECTOR", font = ("times new roman", 22, "bold"), fg = "White", bg = "black")
        l.place(x = 300, y = 6)

        lbl = Label(self.root, text = "Choose below", font = ("times new roman", 14), fg = "white", bg = "black")
        lbl.place(x = 50, y = 100)

        btn_vid = Button(self.root, text = "Video Clip", width = 15, command = self.vid_open, font = ("times new roman", 22, "bold"), fg = "black", bg = "gray", bd = 5, relief = RIDGE, cursor = "hand1")
        btn_vid.place(x = 50, y = 140)

        btn_webcam = Button(self.root, text = "Web Camera", width = 15, command = self.cam_open, font = ("times new roman", 22, "bold"), fg = "black", bg = "gray", bd = 5, relief = RIDGE, cursor = "hand1")
        btn_webcam.place(x = 50, y = 210)

        btn_text = Button(self.root, text = "Convert to Text", command = self.morse2text, width = 18, font = ("times new roman", 22, "bold"), fg = "black", bg = "gray", bd = 5, relief = RIDGE, cursor = "hand1")
        btn_text.place(x = 550, y = 70)

        btn_clear = Button(self.root, text = "Clear text", command = self.clear_frame, width = 18, font = ("times new roman", 22, "bold"), fg = "black", bg = "gray", bd = 5, relief = RIDGE, cursor = "hand1")
        btn_clear.place(x = 550, y = 140)

        btn_speech = Button(self.root, text = "Convert to Speech", command = self.speech, width = 18, font = ("times new roman", 22, "bold"), fg = "black", bg = "gray", bd = 5, relief = RIDGE, cursor = "hand1")
        btn_speech.place(x = 550, y = 210)

    def morse2text(self):
        self.total = []
        string = ""
        c = 0
        cnt = 0
        count = []
        self.tot = ""
        
        for ratio in self.eye_blink_signal:
            if ratio<0.20:
                cnt+= 1
            if ratio>=0.20:
                count.append(cnt)
                cnt = 0

        prev = 0
        a = []

        for j in range(len(count)):
            if prev and count[j]:
                a.append(j)
            prev = count[j]
        for i in range(len(a)):
            j = a[i] = a[i] - i
            count[j-1:j+1] = [count[j-1] + count[j]]
            
        print(count)

        for a in count: 
            if a == 0:
                c+=1
            else:
                if 2<=c<=19:
                    self.total.append("")
                elif 20<=c<=60:
                    self.total.append(" ")
                elif c>60:
                    self.total.append("/")

                c = 0
                if 12<=a<=55: 
                    self.total.append("-")
                elif 1<=a<=11:
                    self.total.append(".")
                elif a>55:
                    self.total.append("*")
                    #if self.total:
                        #self.total.pop()
        self.showDataframe = Frame(self.root, bd = 4, relief = RIDGE, padx= 2)
        self.showDataframe.place(x = 50, y = 300, width = 800, height= 180)

        txt = ""
        for i in self.total:
            txt+=i
        new_txt = txt + " "
        txt = txt.replace("/", " ")
        lblName = Label(self.showDataframe, text = txt, font = ("arial", 16, "bold"))
        lblName.place(x = 3, y = 3)

        self.morseDict={'' : '',
                    '.-': 'a',
                    '-...': 'b',
                    '-.-.': 'c',
                    '-..': 'd',
                    '.': 'e',
                    '..-.': 'f',
                    '--.': 'g',
                    '....': 'h',
                    '..': 'i',
                    '.---': 'j',
                    '-.-': 'k',
                    '.-..': 'l',
                    '--': 'm',
                    '-.': 'n',
                    '---': 'o',
                    '.--.': 'p',
                    '--.-': 'q',
                    '.-.': 'r',
                    '...': 's',
                    '-': 't',
                    '..-': 'u',
                    '...-': 'v',
                    '.--': 'w',
                    '-..-': 'x',
                    '-.--': 'y',
                    '--..': 'z',
                    '.-.-': ' ',
                    }   
        
        for s in new_txt:
            if s==" " or s=="" or s=="/":
                eng = self.morseDict.get(string)
                if eng == None:
                    continue
                self.tot+=eng
                if s == "/":
                    self.tot+=" "
                string = ""
            elif s=="*":
                self.tot = self.tot[:-1]
            else:
                string+=s 
            prev = s
        lblName = Label(self.showDataframe, text = self.tot, font = ("arial", 14, "bold"))
        lblName.place(x = 3, y = 30)
    
    def speech(self):

        # The text that you want to convert to audio
        mytext = self.tot
        if mytext == None:
            return
        tts = gtts.gTTS(mytext, lang="en", slow=False)
        tts.save("txt.mp3")
        playsound("txt.mp3")

    def clear_frame(self):
        for widgets in self.showDataframe.winfo_children():
            widgets.destroy()

    def cam_open(self):
        c = Camera()
        self.eye_blink_signal = c.eye_blink_signal
       

    def vid_open(self):
        v = Video()
        self.eye_blink_signal = v.eye_blink_signal
        

if __name__ == "__main__":
    root = Tk()
    obj = Main_Win(root)
    root.mainloop()



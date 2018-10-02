from tkinter import Tk, Label
from datetime import datetime, timedelta
from re import findall
from time import sleep
import subprocess, sys, os
import threading

DEBUG = True
flag = False

playlist = []
class audioThread(threading.Thread):
    def run(self):
        global playlist
        while True:
            if len(playlist) != 0:
                print(subprocess.check_call(["omxplayer", "/".join(__file__.split("/")[:-1]) + "/" + playlist.pop()]))
            else:
                sleep(0.1)
audioThread().start()

root = Tk()
root.attributes('-fullscreen', not DEBUG)
timeFrom = 2600000
currentColour = "#000000"

if DEBUG:
    eta = datetime.now()+timedelta(seconds=10)
else:
    eta = datetime(2018, 10, 26, 15, 15, 00)

def updateTHEPROGRAM(event):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-U', 'git+git://github.com/Icia200/underpressure'])
    os.execv(sys.executable, ["python", os.path.realpath(__file__)])
root.bind("<Button-1>", updateTHEPROGRAM)

def pad(l):
    while len(l) <= 5:
        l.insert(1, "00")
    return l


def stop(nextCycle):
    timel.configure(fg=nextCycle)
    if nextCycle == "red":
        root.after(500, lambda x="white":stop(x))
    else:
        root.after(500, lambda x="red":stop(x))


def update():
    global currentColour, flag
    newTime   = eta - datetime.now()
    percent   = (timeFrom-(newTime.seconds+newTime.days*3600*24))/timeFrom*255
    newColour = "#"+str(hex(round(percent))[2:].zfill(2))+"0000"

    if newColour != currentColour:
        title.configure(bg=newColour)
        timel.configure(bg=newColour)
        root .configure(bg=newColour)
        currentColour = newColour

    newTime = pad([x.zfill(2)[0:2] for x in findall(r"[\w']+", str(newTime))])
    del newTime[1], newTime[-1]
    timel.configure(text="{0} Days\n{1}:{2}:{3}".format(*newTime))

    if "".join(newTime) == "00000000":
        stop("red")
        if not flag:
            playlist.append("Pressure.mp3")
            flag = True
    else:
        root.after(200, update)


title = Label(font=("ansifixed", 50), bg="black", fg="white", text="ICT Deadline (updateMe):")
timel = Label(font=("ansifixed", 90), bg="black", fg="white", text="")

title.pack(expand=True)
timel.pack(expand=True)

update()
root.mainloop()

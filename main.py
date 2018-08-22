from tkinter import Tk, Frame, Button, BOTH
import time
from threading import Thread

def onClick(root, cliptext):
    print("copied ", cliptext)
    root.clipboard_clear()
    root.clipboard_append(cliptext)

def updateClipboard(root, clipboardContent, f):

    truncateButtonLength = 30
    maxClippings = 10

    while True:
        allButtons = [button for button in f.children.values()]
        #print("buttons are ", len(allButtons))
        time.sleep(0.1)
        cliptextShort = cliptext = root.clipboard_get()

        if len(cliptext) > truncateButtonLength:
            cliptextShort = cliptext[:truncateButtonLength]+" ..."
        #print("in loop")
        if cliptext not in clipboardContent:
            clipboardContent.add(cliptext)

            if len(allButtons) == maxClippings:
                #print("destroying first button!")
                allButtons[0].destroy()

            b = Button(f, text=cliptextShort, cursor="plus", wraplength=100, command=lambda cliptext=cliptext: onClick(root, cliptext))
            b.pack(fill=BOTH)
            root.lift()

def startMain():
    clipboardContent = set()

    root = Tk()
    root.title("My clipboard")

    f = Frame(root, height=500, width=500)
    f.pack_propagate(0) # don't shrink
    f.pack()

    t = Thread(target=updateClipboard, args=(root, clipboardContent, f))
    t.start()
    root.mainloop()

if __name__ == '__main__':
    startMain()

from tkinter import *
import time
from threading import Thread

def updateClipboard(T, root, clipboardContent):
    while True:
        time.sleep(1)
        cliptext = root.clipboard_get()
        print("in loop")
        if cliptext not in clipboardContent:
            clipboardContent.add(cliptext)
            T.insert(END, cliptext + "\n\n")
            T.pack()
            root.lift()

def startMain():
    clipboardContent = set()

    root = Tk()
    T = Text(root)
    t = Thread(target=updateClipboard, args=(T, root, clipboardContent))
    t.start()
    root.mainloop()

if __name__ == '__main__':
    startMain()

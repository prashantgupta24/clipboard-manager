from tkinter import *
import time
from threading import Thread

def updateClipboard(T, root, clipboardContent):
    while True:


        time.sleep(0.5)

        cliptext = root.clipboard_get()
        #print("in loop")
        if cliptext not in clipboardContent:
            clipboardContent.add(cliptext)
            T.insert(END, cliptext + "\n")
            T.pack()
            root.lift()

def startMain():

    clipboardContent = set()

    root = Tk()

    T = Text(root)
    t = Thread(target=updateClipboard, args=(T, root, clipboardContent))
    t.start()
    root.mainloop()
# def callback(event):
#     print("clicked at", event.x, event.y)
#
# def key(event):
#     print("pressed", repr(event.char))
#
# frame = Frame(root, width=200, height=200)
# frame.bind("<Key>", key)
# frame.bind("<Button-1>", callback)
# frame.pack()
if __name__ == '__main__':
    startMain()

from tkinter import Tk, Frame, Button, BOTH, Widget
import time
from threading import Thread

def onClick(root, cliptext):
    #print("copied ", cliptext)
    root.clipboard_clear()
    root.clipboard_append(cliptext)

def updateClipboard(root, clipboardContent, f):

    truncateTextLength = 30
    maxClippings = 10

    while True:
        allButtons = [button for button in f.children.values()]
        #print("buttons are ", len(allButtons))
        time.sleep(0.1)
        cliptext = root.clipboard_get()

        cliptext = "".join([c for c in cliptext if ord(c) <= 65535])

        if not cliptext:
            continue

        if len(cliptext) > truncateTextLength:
            cliptextShort = cliptext[:truncateTextLength]+" ..."
        else:
            cliptextShort = cliptext
        #print("in loop")
        if cliptext not in clipboardContent:
            clipboardContent.add(cliptext)
            # print(cliptext)
            # print([ord(x) for x in cliptext])

            if len(allButtons) == maxClippings:
                #print("destroying first button!")
                allButtons[0].destroy()

            b = Button(f, text=cliptextShort, cursor="plus", wraplength=100, command=lambda cliptext=cliptext: onClick(root, cliptext))
            b.pack(fill=BOTH)
            root.lift()

def startMain():
    clipboardContent = set()

    root = Tk()
    root.title("Clippy")

    f = Frame(root, height=500, width=500)
    f.pack_propagate(0) # don't shrink
    f.pack()

    Thread(target=updateClipboard, args=(root, clipboardContent, f)).start()
    Widget.update(root)
    root.mainloop()

if __name__ == '__main__':
    startMain()

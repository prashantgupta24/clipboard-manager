from tkinter import Tk, Frame, Button, BOTH
import time
from threading import Thread

def onClick(root, cliptext):
    #print("clicked!")
    root.clipboard_clear()
    root.clipboard_append(cliptext)

def updateClipboard(root, clipboardContent, f):
    while True:
        # for child in f.children.values():
        #     #print(dir(child))
        #     child.destroy()
        allButtons = [button for button in f.children.values()]
        #print("number is ", len(allButtons))
        time.sleep(0.1)
        cliptext = root.clipboard_get()
        #print("in loop")
        if cliptext not in clipboardContent and len(cliptext) < 200:
            clipboardContent.add(cliptext)
            if len(allButtons) == 2:
                print("destroying!")
                allButtons[0].destroy()
            b = Button(f, text=cliptext, cursor="plus", wraplength=100, command=lambda: onClick(root, cliptext))
            b.pack(fill=BOTH)
            #b.grid(row=i, column=0)
            root.lift()
        else:
            #TODO trimming and saving full text in dict
            pass

def startMain():
    clipboardContent = set()

    root = Tk()
    f = Frame(root, height=500, width=500)
    f.pack_propagate(0) # don't shrink
    f.pack()

    t = Thread(target=updateClipboard, args=(root, clipboardContent, f))
    t.start()
    root.mainloop()

if __name__ == '__main__':
    startMain()

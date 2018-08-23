from tkinter import Tk, Frame, Button, BOTH

class Clippy(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent, height=500, width=500)
        self.pack_propagate(0)
        self.pack()

        #self.parent = parent
        self.clipboardContent = set()
        self.pollingFrequencyMs = 100
        self.truncateTextLength = 30
        self.maxClippingsOnApp = 10
        self.debug = False

        self.updateClipboard()

    def updateClipboard(self):

        cliptext = self.clipboard_get()

        #Handle empty clipboard content
        if not cliptext:
            return

        #Removing all characters > 65535 (that's the range for tkinter)
        cliptext = "".join([c for c in cliptext if ord(c) <= 65535])

        #Clipping content to loop pretty
        if len(cliptext) > self.truncateTextLength:
            cliptextShort = cliptext[:self.truncateTextLength]+" ..."
        else:
            cliptextShort = cliptext

        #Updating screen if new content found
        if cliptext not in self.clipboardContent:
            self.clipboardContent.add(cliptext)

            if self.debug:
                print(cliptext)
                print([ord(x) for x in cliptext])

            #Removing the oldest entry
            allButtons = [button for button in self.children.values()]
            if len(allButtons) == self.maxClippingsOnApp:
                allButtons[0].destroy()

            b = Button(self, text=cliptextShort, cursor="plus", wraplength=100, command=lambda cliptext=cliptext: self.onClick(cliptext))
            b.pack(fill=BOTH)
            #self.parent.lift()

        self.after(ms=self.pollingFrequencyMs, func=self.updateClipboard)

    def onClick(self, cliptext):
        if self.debug:
            print("copied ", cliptext)

        self.clipboard_clear()
        self.clipboard_append(cliptext)

if __name__ == '__main__':
    root = Tk()
    root.title("Clippy")
    #root.lift()
    #root.attributes("-topmost", True)
    Clippy(root).mainloop()

from tkinter import Tk, Frame, Button, BOTH, Menu, TclError

class Clippy(Frame):
    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self, parent, height=500, width=500)
        parent.title("Clippy")
        parent.resizable(False, False)
        self.pack_propagate(0)
        self.pack()
        self.initMenu()

        self.clipboardContent = set()
        self.pollingFrequencyMs = 100
        self.truncateTextLength = 100
        self.maxClippingsOnApp = 10
        self.debug = False

        self.updateClipboard()

    def initMenu(self):
        menubar = Menu(self)
        optionsMenu = Menu(menubar, tearoff=0)
        optionsMenu.add_command(label="Clear all (except last)", command=self.clearAllButtons)
        optionsMenu.add_checkbutton(label="Always on top", command=self.toggleAlwaysOnTop)
        menubar.add_cascade(label="Options", menu=optionsMenu)
        self.parent.config(menu=menubar)

    def updateClipboard(self):

        try:
            cliptext = self.clipboard_get()
            #Handle empty clipboard content
            if not cliptext:
                return

            cliptext, cliptextShort = self.cleanClipText(cliptext=cliptext)
            #Updating screen if new content found
            if cliptextShort not in self.clipboardContent:
                self.clipboardContent.add(cliptextShort)
                self.cleanupOldButtons()
                Button(self, text=cliptextShort, cursor="plus", wraplength = 500, command=lambda cliptext=cliptext: self.onClick(cliptext)).pack(fill=BOTH)

                self.update()
                self.parent.update()
                self.pack()
                self.lift()
                self.parent.lift()

        except TclError:
            pass #nothing on clipboard

        self.after(ms=self.pollingFrequencyMs, func=self.updateClipboard)

    def cleanupOldButtons(self):
        #Removing the oldest entry
        allButtons = self.getAllButtons()
        if self.debug:
            print([button["text"] for button in allButtons])
        if len(allButtons) == self.maxClippingsOnApp:
            self.clipboardContent.discard(allButtons[0].cget("text"))
            if self.debug:
                print(self.clipboardContent)
            allButtons[0].destroy()

    def cleanClipText(self, cliptext):
        #Removing all characters > 65535 (that's the range for tkinter)
        cliptext = "".join([c for c in cliptext if ord(c) <= 65535])
        #Clipping content to loop pretty
        if len(cliptext) > self.truncateTextLength:
            cliptextShort = cliptext[:self.truncateTextLength]+" ..."
        else:
            cliptextShort = cliptext
        #Removing new lines from short text
        cliptextShort = cliptextShort.replace("\n", "").strip()
        return (cliptext, cliptextShort)

    def onClick(self, cliptext):
        if self.debug:
            print("copied ", cliptext)
        self.clipboard_clear()
        self.clipboard_append(cliptext)

    def getAllButtons(self):
        return [button for button in self.children.values() if isinstance(button, Button)]

    def clearAllButtons(self):
        allButtons = self.getAllButtons()
        for button in allButtons:
            button.destroy()
        self.clipboardContent = set()
        #self.clipboard_clear()

    def toggleAlwaysOnTop(self):
        if self.parent.attributes("-topmost") == 0:
            self.parent.attributes("-topmost", 1)
        else:
            self.parent.attributes("-topmost", 0)

if __name__ == '__main__':
    root = Tk()
    Clippy(root).mainloop()

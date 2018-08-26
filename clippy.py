from tkinter import Tk, Frame, BOTH, Menu, TclError, Label, RAISED, StringVar, SUNKEN

class Clippy(Frame):
    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self, parent, height=600, width=600)
        parent.title("Clippy")
        parent.resizable(False, False)
        self.pack_propagate(0)
        self.pack()
        self.initMenu()

        self.clipboardContent = set()
        self.pollingFrequencyMs = 100
        self.truncateTextLength = 100
        self.maxClippingsOnApp = 10
        self.labelArray = []
        self.labelIterVal = 0
        self.debug = False

        self.createLayout()
        self.updateClipboard()

    def initMenu(self):
        menubar = Menu(self)
        optionsMenu = Menu(menubar, tearoff=0)
        optionsMenu.add_command(label="Clear all (except last)", command=self.clearAll)
        optionsMenu.add_checkbutton(label="Always on top", command=self.toggleAlwaysOnTop)
        menubar.add_cascade(label="Options", menu=optionsMenu)
        self.parent.config(menu=menubar)

    def createLayout(self):
        for i in range(self.maxClippingsOnApp):
            l = Label(self, text="", cursor="plus", relief=RAISED, pady=5,  wraplength=500)
            l.pack(fill=BOTH, padx=5, pady=2, expand=1)
            l.bind("<Button-1>", lambda e, labelNum=i: self.onClick(labelNum))
            self.labelArray.append(l)

    def updateClipboard(self):
        try:
            cliptext = self.clipboard_get()
            #Handle empty clipboard content
            if not cliptext:
                return

            cliptext, cliptextShort = self.cleanClipText(cliptext=cliptext)
            #Updating screen if new content found
            if cliptextShort not in self.clipboardContent:
                #print(cliptextShort)
                self.clipboardContent.add(cliptextShort)

                if self.labelIterVal == self.maxClippingsOnApp:
                    self.labelIterVal = 0

                label = self.labelArray[self.labelIterVal]
                labelText = label["text"]
                if labelText in self.clipboardContent:
                    self.clipboardContent.discard(labelText)
                label["text"] = cliptextShort
                self.labelIterVal += 1

                self.update()
                self.parent.update()
                self.pack()
                self.lift()
                self.parent.lift()

        except TclError:
            pass #nothing on clipboard

        self.after(ms=self.pollingFrequencyMs, func=self.updateClipboard)

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

    def onClick(self, labelNum):
        label = self.labelArray[labelNum]
        if self.debug:
            print("copied ", label["text"])
        self.clipboard_clear()
        self.clipboard_append(label["text"])
        label["relief"] = SUNKEN
        self.after(ms=100, func=lambda label=label: self.animateClick(label))

    def animateClick(self, label):
        label["relief"] = RAISED

    def clearAll(self):
        for label in range(self.labelArray):
            label["text"] = ""
        self.clipboardContent = set()

    def toggleAlwaysOnTop(self):
        if self.parent.attributes("-topmost") == 0:
            self.parent.attributes("-topmost", 1)
        else:
            self.parent.attributes("-topmost", 0)

if __name__ == '__main__':
    root = Tk()
    Clippy(root).mainloop()

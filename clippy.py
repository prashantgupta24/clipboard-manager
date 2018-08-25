from tkinter import Tk, Frame, Button, BOTH, Menu, TclError, Label, RAISED, StringVar

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
        optionsMenu.add_command(label="Clear all (except last)", command=self.clearAllButtons)
        optionsMenu.add_checkbutton(label="Always on top", command=self.toggleAlwaysOnTop)
        menubar.add_cascade(label="Options", menu=optionsMenu)
        self.parent.config(menu=menubar)

    def createLayout(self):

        for i in range(self.maxClippingsOnApp):
            # var = StringVar()
            # var.set('ddd')
            # self.labelVar.append(var)
            # self.var = var
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
                self.clipboardContent.add(cliptextShort)
                if self.labelIterVal == self.maxClippingsOnApp:
                    self.labelIterVal = 0
                #self.cleanupOldButtons()
                #Label(self, text=cliptextShort, cursor="plus", relief=RAISED, pady=5,  wraplength=500).pack(fill=BOTH, expand=1)
            #, command=lambda cliptext=cliptext: self.onClick(cliptext)

                # var = StringVar()
                # var.set(cliptextShort)
                label = self.labelArray[self.labelIterVal]
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

    def onClick(self, labelNum):
        #if self.debug:
        print(labelNum)
        label = self.labelArray[labelNum]
        print("copied ", label["text"])
        # self.clipboard_clear()
        # self.clipboard_append(cliptext)

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

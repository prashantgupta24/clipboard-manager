from tkinter import Tk, Frame, BOTH, Menu, TclError, Label, RAISED, SUNKEN, SOLID, messagebox
import pyperclip

class Clippy(Frame):
    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self, parent, height=600, width=600)
        parent.title("Clippy")
        parent.resizable(False, False)
        self.pack_propagate(0)
        self.pack()

        self.initDefaultValues()
        self.pollingFrequencyMs = 100
        self.truncateTextLength = 100
        self.maxClippingsOnApp = 10
        self.labelArray = []
        self.debug = False

        self.initMenu()

    def initDefaultValues(self):
        self.clipboardContent = set()
        self.clipboardContentMapping = {}
        self.labelUpdateVal = 0

    def initMenu(self):
        menubar = Menu(self)
        optionsMenu = Menu(menubar, tearoff=0)
        optionsMenu.add_checkbutton(label="Always on top", command=self.toggleAlwaysOnTop)
        optionsMenu.add_command(label="Clear all (except last)", command=self.clearAll)
        menubar.add_cascade(label="Options", menu=optionsMenu)
        self.parent.config(menu=menubar)

    def createLayout(self):
        for i in range(self.maxClippingsOnApp):
            l = Label(self, text="", cursor="plus", relief=RAISED, pady=5,  wraplength=500)
            l.pack(fill=BOTH, padx=5, pady=2, expand=1)
            l.bind("<Button-1>", lambda e, labelNum=i: self.onClick(labelNum))
            self.labelArray.append({
                "label": l,
                "text": "", #only for debugging purposes, only label["text"] matters
                "clickCount": 0,
                "updated": 0,
            })

    def updateClipboard(self):
        try:
            #cliptext = self.clipboard_get()
            cliptext = pyperclip.paste()
            self.processClipping(cliptext=cliptext)

        except Exception as e:
            print("ERROR!! -> ", e)

        if self.debug:
            self.after(ms=5000, func=self.updateClipboard)
        else:
            self.after(ms=self.pollingFrequencyMs, func=self.updateClipboard)

    def processClipping(self, cliptext):
        if self.debug:
            print("Called function, got ->", cliptext)

        cliptext, cliptextShort = self.cleanClipText(cliptext=cliptext)
        #Updating screen if new content found
        if cliptext not in self.clipboardContent and cliptextShort:

            if cliptextShort not in self.clipboardContentMapping: #new clipping altogether
                self.labelUpdateVal += 1
                labelArrsortByUpdated = sorted(self.labelArray, key=lambda t:t["updated"])
                labelArrsortByClicked = sorted(labelArrsortByUpdated, key=lambda t:t["clickCount"])

                labelElem = labelArrsortByClicked[0]
                label = labelElem["label"]
                labelText = label["text"]
                if labelText in self.clipboardContentMapping:
                    self.clipboardContent.discard(self.clipboardContentMapping[labelText])
                    self.clipboardContentMapping.pop(labelText)
                label["text"] = cliptextShort
                label["relief"] = RAISED
                labelElem["updated"] = self.labelUpdateVal
                labelElem["text"] = cliptextShort
                labelElem["clickCount"] = 0
            else: # New clipping but shortened version is the same, so discard previous value
                self.clipboardContent.discard(self.clipboardContentMapping[cliptextShort])

            self.clipboardContent.add(cliptext)
            self.clipboardContentMapping[cliptextShort] = cliptext

            self.update()
            self.parent.update()
            self.pack()
            # Following commands can bring focus to the app on each update, but it was not very desirable
            # self.lift()
            # self.parent.lift()

    def cleanClipText(self, cliptext):
        #Removing all characters > 65535 (that's the range for tcl)
        cliptext = "".join([c for c in cliptext if ord(c) <= 65535])
        #Clipping content to look pretty
        if len(cliptext) > self.truncateTextLength:
            cliptextShort = cliptext[:self.truncateTextLength]+" ..."
        else:
            cliptextShort = cliptext
        #Removing new lines from short text
        cliptextShort = cliptextShort.replace("\n", "").strip()
        return (cliptext, cliptextShort)

    def onClick(self, labelNum):
        labelElem = self.labelArray[labelNum]
        label = labelElem["label"]
        if label["text"] == "":
            return
        if self.debug:
            print(labelElem)
            print("copied ", self.clipboardContentMapping[label["text"]])
        # self.clipboard_clear()
        # self.clipboard_append(self.clipboardContentMapping[label["text"]])
        pyperclip.copy(self.clipboardContentMapping[label["text"]])
        label["relief"] = SUNKEN
        labelElem["clickCount"] = 1
        self.after(ms=100, func=lambda label=label: self.animateClick(label))

    def animateClick(self, label):
        label["relief"] = SOLID

    def clearAll(self):
        result = messagebox.askyesno("Clear All", "Are you sure you want to clear all clippings from the application?", icon='warning')
        if result:
            for labelElem in self.labelArray:
                labelElem["label"]["text"] = ""
                labelElem["label"]["relief"] = RAISED
                labelElem["text"] = ""
                labelElem["clickCount"] = 0
                labelElem["updated"] = 0
            self.initDefaultValues()

    def toggleAlwaysOnTop(self):
        if self.parent.attributes("-topmost") == 0:
            self.parent.attributes("-topmost", 1)
        else:
            self.parent.attributes("-topmost", 0)

if __name__ == '__main__':
    root = Tk()
    Clippy = Clippy(root)
    Clippy.createLayout()
    Clippy.updateClipboard()
    Clippy.mainloop()

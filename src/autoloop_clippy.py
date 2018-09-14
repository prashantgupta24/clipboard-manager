from tkinter import Tk
import pyperclip

import clippy

class TestClippyVisual():

    def __init__(self):
        self.iterVal = 0
        self.debug = True

        self.root = Tk()
        self.ClippyTestClass = clippy.Clippy(self.root)
        self.ClippyTestClass.maxClippingsOnApp = 5
        self.ClippyTestClass.createLayout()
        self.testClippyVisual()
        self.ClippyTestClass.updateClipboard()
        self.ClippyTestClass.mainloop()

    def testClippyVisual(self):
        cliptext = "cliptext-" + str(self.iterVal)
        self.iterVal += 1
        pyperclip.copy(cliptext)
        print("sent to clippy -> ", cliptext)
        if self.debug:
            print("*"*100)
            print("clipboardContent -> ", self.ClippyTestClass.clipboardContent)
            print()
            print("clipboardContentMapping -> ", self.ClippyTestClass.clipboardContentMapping)
            print()
            print("labelArray :")
            [print(list(labelElem.items())) for labelElem in self.ClippyTestClass.labelArray]
            print("*"*100)
        self.root.after(ms=1500, func=self.testClippyVisual)

if __name__ == '__main__':
    TestClippyVisual()

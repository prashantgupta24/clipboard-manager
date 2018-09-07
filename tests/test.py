import time
import random
import unittest

import clippy

class TestClippy(unittest.TestCase):

    def setUp(self):
        self.root = clippy.Tk()
        self.ClippyTestClass = clippy.Clippy(self.root)
        self.ClippyTestClass.maxClippingsOnApp = random.randint(2,10)
        self.ClippyTestClass.createLayout()
        self.longLoopIterationVal = random.randint(100,300)

        self.cliptextArr= {
            "hello":("hello", "hello"),
            "h" + chr(120000):("h", "h"),
            "a"*(self.ClippyTestClass.truncateTextLength+1):("a"*(self.ClippyTestClass.truncateTextLength+1), "a"*self.ClippyTestClass.truncateTextLength+" ..."),
            "abc\nde\nf":("abc\nde\nf", "abcdef"),
            "space after   ":("space after   ", "space after"),
            "  space before":("  space before", "space before")
        }

    # def tearDown(self):
    #     self.root.destroy()

    def testCleanClipText(self):
        for cliptext, expectedVal in self.cliptextArr.items():
            self.assertEqual(self.ClippyTestClass.cleanClipText(cliptext=cliptext), expectedVal)
        #invalid cases
        self.assertEqual(self.ClippyTestClass.cleanClipText(cliptext="  "), ("  ", ""))
        self.assertEqual(self.ClippyTestClass.cleanClipText(cliptext=" \n \n \n"), (" \n \n \n", ""))

    def testProcessClippingDefinedInput(self):
        i = 0
        for cliptext in self.cliptextArr.keys():
            cliptext, cliptextShort = self.ClippyTestClass.cleanClipText(cliptext=cliptext)
            self.ClippyTestClass.processClipping(cliptext=cliptext)
            labelElem = self.ClippyTestClass.labelArray[i % self.ClippyTestClass.maxClippingsOnApp]

            self.assertIn(cliptext, self.ClippyTestClass.clipboardContent, "Content not found in clipboard content data structure")
            self.assertIn(cliptextShort, self.ClippyTestClass.clipboardContentMapping, "Content not found in clipboard content mapping data structure")
            self.assertEqual(self.ClippyTestClass.clipboardContentMapping[cliptextShort], cliptext)
            self.assertEqual(labelElem["label"]["text"], cliptextShort, "Label not created correctly")
            i+=1
            #self.assertIn(cliptextShort, [label["text"] for label in self.ClippyTestClass.labelArray if label["text"] == cliptextShort], "Label not created correctly")


    def testProcessClippingLongLoop(self):
        for i in range(self.longLoopIterationVal):
            cliptext = "cliptext - " + str(i)
            self.ClippyTestClass.processClipping(cliptext=cliptext)
            labelElem = self.ClippyTestClass.labelArray[i % self.ClippyTestClass.maxClippingsOnApp]

            self.assertEqual(labelElem["label"]["text"], cliptext, "Label not created correctly")
            self.assertEqual(labelElem["updated"], i+1, "Update value for label not set correctly")
            #time.sleep(0.1)

    def testOnClickFunctionLongLoop(self):
        labelsClicked = [random.randint(0, self.ClippyTestClass.maxClippingsOnApp-1), random.randint(0, self.ClippyTestClass.maxClippingsOnApp-1)]
        print("labelsClicked with size", labelsClicked, self.ClippyTestClass.maxClippingsOnApp)
        j = loopVal = 0
        for i in range(self.longLoopIterationVal):
            cliptext = "cliptext - " + str(i)
            self.ClippyTestClass.processClipping(cliptext=cliptext)
            if i in labelsClicked:
                self.ClippyTestClass.onClick(i)

            if i >= self.ClippyTestClass.maxClippingsOnApp:
                j = (i + loopVal) % self.ClippyTestClass.maxClippingsOnApp
                while j in labelsClicked:
                    j += 1
                    loopVal += 1
            else:
                j = i

            labelElem = self.ClippyTestClass.labelArray[j % self.ClippyTestClass.maxClippingsOnApp]

            self.assertEqual(labelElem["label"]["text"], cliptext, "Label not created correctly")
            self.assertEqual(labelElem["updated"], i+1, "Update value for label not set correctly")
            #time.sleep(0.1)

    def testOnClickFunction(self):
        i = 0
        for cliptext in self.cliptextArr.keys():
            cliptext, _ = self.ClippyTestClass.cleanClipText(cliptext=cliptext)
            self.ClippyTestClass.processClipping(cliptext=cliptext)
            self.ClippyTestClass.clipboard_clear()
            self.ClippyTestClass.onClick(i % self.ClippyTestClass.maxClippingsOnApp)
            #print("CLIPBOARD ->", self.ClippyTestClass.clipboard_get())
            # print([label["text"] for label in self.ClippyTestClass.labelArray])
            self.assertEqual(self.ClippyTestClass.clipboard_get(), cliptext, "Clipboard content not matching")
            i+=1

    def testOnClickFunctionLongLoopWithClicks(self):
        for i in range(self.longLoopIterationVal):
            labelIterator = i % self.ClippyTestClass.maxClippingsOnApp
            cliptext = "cliptext - " + str(labelIterator)
            self.ClippyTestClass.processClipping(cliptext=cliptext)
            self.ClippyTestClass.clipboard_clear()
            self.ClippyTestClass.onClick(labelIterator)
            labelElem = self.ClippyTestClass.labelArray[labelIterator]

            self.assertEqual(self.ClippyTestClass.clipboard_get(), cliptext, "Clipboard content not matching")
            self.assertEqual(labelElem["label"]["text"], cliptext, "Label not created correctly")
            self.assertEqual(labelElem["clickCount"], int(i/self.ClippyTestClass.maxClippingsOnApp) + 1, "Label click count not proper")
            self.assertEqual(labelElem["updated"], labelIterator+1, "Update value for label not set correctly")
            #time.sleep(0.1)

import unittest
import clippy

class TestClippy(unittest.TestCase):

    def setUp(self):
        self.root = clippy.Tk()
        self.ClippyTestClass = clippy.Clippy(self.root)
        self.cliptextArr= {
            "hello":("hello", "hello"),
            "h" + chr(120000):("h", "h"),
            "a"*(self.ClippyTestClass.truncateTextLength+1):("a"*(self.ClippyTestClass.truncateTextLength+1), "a"*self.ClippyTestClass.truncateTextLength+" ..."),
            "abc\nde\nf":("abc\nde\nf", "abcdef"),
            "hello   ":("hello   ", "hello"),
            "  hello":("  hello", "hello")
        }

    def testCleanClipText(self):
        for cliptext, expectedVal in self.cliptextArr.items():
            self.assertEqual(self.ClippyTestClass.cleanClipText(cliptext=cliptext), expectedVal)
        # self.assertEqual(self.ClippyTestClass.cleanClipText(cliptext="hello"), ("hello", "hello"))
        # self.assertEqual(self.ClippyTestClass.cleanClipText(cliptext="h" + chr(120000)), ("h", "h"))
        # self.assertEqual(self.ClippyTestClass.cleanClipText(cliptext="a"*(self.ClippyTestClass.truncateTextLength+1)), ("a"*(self.ClippyTestClass.truncateTextLength+1), "a"*self.ClippyTestClass.truncateTextLength+" ..."))
        # self.assertEqual(self.ClippyTestClass.cleanClipText(cliptext="abc\nde\nf"), ("abc\nde\nf", "abcdef"))
        # self.assertEqual(self.ClippyTestClass.cleanClipText(cliptext="hello   "), ("hello   ", "hello"))
        # self.assertEqual(self.ClippyTestClass.cleanClipText(cliptext="  hello"), ("  hello", "hello"))
        self.assertEqual(self.ClippyTestClass.cleanClipText(cliptext="  "), ("  ", ""))
        self.assertEqual(self.ClippyTestClass.cleanClipText(cliptext=" \n \n \n"), (" \n \n \n", ""))

    def testProcessClipping(self):
        #cliptextArr=["hello", "This is a random string", "h" + chr(120000), "a"*(self.ClippyTestClass.truncateTextLength+1)]
        i = 0
        for cliptext in self.cliptextArr.keys():
            cliptext, cliptextShort = self.ClippyTestClass.cleanClipText(cliptext=cliptext)
            self.ClippyTestClass.processClipping(cliptext=cliptext)
            self.assertIn(cliptext, self.ClippyTestClass.clipboardContent, "Content not found in clipboard content data structure")
            self.assertIn(cliptextShort, self.ClippyTestClass.clipboardContentMapping, "Content not found in clipboard content mapping data structure")
            self.assertEqual(self.ClippyTestClass.clipboardContentMapping[cliptextShort], cliptext)
            #self.assertIn(cliptextShort, [label["text"] for label in self.ClippyTestClass.labelArray if label["text"] == cliptextShort], "Label not created correctly")
            label = self.ClippyTestClass.labelArray[i]
            self.assertEqual(label["text"], cliptextShort, "Label not created correctly")
            i+=1

    def testOnClickFunction(self):
        #cliptextArr=["hello", "This is a random string", "h" + chr(120000), "a"*(self.ClippyTestClass.truncateTextLength+1)]
        i = 0
        for cliptext in self.cliptextArr.keys():
            cliptext, _ = self.ClippyTestClass.cleanClipText(cliptext=cliptext)
            self.ClippyTestClass.processClipping(cliptext=cliptext)
            self.ClippyTestClass.clipboard_clear()
            self.ClippyTestClass.onClick(i)
            #print("CLIPBOARD ->", self.ClippyTestClass.clipboard_get())
            # print([label["text"] for label in self.ClippyTestClass.labelArray])
            self.assertEqual(self.ClippyTestClass.clipboard_get(), cliptext)
            i+=1

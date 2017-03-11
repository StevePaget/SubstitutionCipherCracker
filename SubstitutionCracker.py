from tkinter import *
import random


class App:
    def __init__(self,master):
        mainframe = Frame(master)
        mainframe.grid(row=0, column=0)
        self.ciphertextContents = ""
        self.topLabel = Label(mainframe, text="Enter encrypted here:")
        self.topLabel.grid(row=0, column=0, columnspan=10, sticky=W)


        self.letterFrequencies = Button(mainframe, text="Show Letter Frequencies", command=self.showLetterFrequencies)
        self.letterFrequencies.grid(row=0, column=17, columnspan=5)

        self.vowelTrowel = Button(mainframe, text="Show Vowel Trowel", command=self.showVowelTrowel)
        self.vowelTrowel.grid(row=0, column=22, columnspan=5)

        self.entryBox = Text(mainframe, height=10, font="courier", bd=2, selectborderwidth=3)
        self.entryBox.grid(row=1, column=0, columnspan=16, sticky=W + E)

        self.decryptedbox = Text(mainframe, height=10, font="courier",bd=2)
        self.decryptedbox.grid(row=3, column=0, columnspan=16, sticky=W + E)

        self.reformatCiphertextButton = Button(mainframe, text="Reformat", command=self.reformatCiphertext)
        self.reformatCiphertextButton.grid(row=0, column=10, columnspan=6, sticky=E)

        self.nextlabel = Label(mainframe, text="Decrypted text appears here:")
        self.nextlabel.grid(row=2, column=0, columnspan=16, sticky=W)


        self.frequencyGraph = Canvas(mainframe, width=450, height=400)
        self.frequencyGraph.grid(row=1, column=18, columnspan=11, rowspan=5)

        self.blankbox = Label(mainframe, width=150, height=1, bd=5)
        self.blankbox.grid(row=4,column=0,columnspan=26)
        
        self.swaptableLabel = Label(mainframe, text="Enter your guesses of letter swaps here:")
        self.swaptableLabel.grid(row=6, column=0, columnspan=26)

        bottomframe = Frame(master)
        bottomframe.grid(row=3, column=0)
        self.topletters = []
        for x in range(26):
            self.topletters.append(
                Label(bottomframe, text=chr(65 + x), width=3, font="courier").grid(row=6, column=x, sticky=W))

        self.bottomletters = []
        self.mappings=[StringVar() for x in range(26)]
        self.oldMappings = ["" for x in range(26)]
        for mapping in self.mappings:
            mapping.trace("w",self.checkentries)
        for x in range(26):
            self.bottomletters.append(
                Entry(bottomframe, width=3, font="courier", justify=CENTER, textvariable=self.mappings[x]).grid(row=7,
                                                                                                                column=x,
                                                                                                                sticky=W))

        self.blankbox = Label(bottomframe, width=150, height=1, bd=5).grid(row=9, column=0, columnspan=26)

        self.go = Button(bottomframe, text="Decrypt!", command=self.autoDecrypt)
        self.go.grid(row=8,column=1,columnspan=9)
        self.random = Button(bottomframe, text="Make Random Key", command=self.randomKey)
        self.random.grid(row=8,column=8,columnspan=9)
        self.clear = Button(bottomframe, text="Clear Key", command=self.clearKey)
        self.clear.grid(row=8,column=15,columnspan=9)
        
        self.contents = self.entryBox.get(1.0, END)
        self.entryBox.bind("<Key>", self.letterEntered)        
        self.entryBox.bind("<FocusOut>", self.letterEntered)

        self.entryBox.bind("<Motion>", self.onMoveEntry)
        self.decryptedbox.bind("<Motion>", self.onMoveDecrypt)


    def autoDecrypt(self):
        print("clicked")

    def reformatCiphertext(self):
        # go through encrypted text and remove spaces & punctuation. Update ciphertext box
        self.ciphertextContents = self.entryBox.get(1.0, END)
        self.ciphertextContents = self.ciphertextContents.replace(" ", "")
        self.ciphertextContents = self.ciphertextContents.replace("\n", "")
        self.ciphertextContents = self.ciphertextContents.upper()
        newCipherText = ""
        letterCount = 0
        for letter in self.ciphertextContents:
            letterNum = ord(letter) - 65
            if letterNum >= 0 and letterNum <= 26:
                newCipherText += letter
                letterCount+=1
                if letterCount % 5==0:
                    newCipherText +=" "
        self.entryBox.delete(1.0, END)
        self.entryBox.insert(1.0, newCipherText)
        self.letterEntered(None)

    def onMoveDecrypt(self, a):
        self.entryBox.tag_delete("hl")
        self.decryptedbox.tag_delete("hl")
        self.entryBox.tag_config("all", background="white")
        self.decryptedbox.tag_config("all", background="white")
        self.decryptedbox.tag_add("hl", CURRENT, "%s+2c" % CURRENT)
        self.decryptedbox.tag_configure("hl", background="light green")
        hlRange = self.decryptedbox.tag_ranges("hl")
        self.entryBox.tag_add("hl", hlRange[0], hlRange[1])
        self.entryBox.tag_configure("hl", background="light green")

    def onMoveEntry(self, a):
        self.entryBox.tag_delete("hl")
        self.decryptedbox.tag_delete("hl")
        self.entryBox.tag_config("all", background="white")
        self.decryptedbox.tag_config("all", background="white")
        self.entryBox.tag_add("hl", CURRENT, "%s+2c" % CURRENT)
        self.entryBox.tag_configure("hl", background="light blue")
        hlRange = self.entryBox.tag_ranges("hl")
        self.decryptedbox.tag_add("hl", hlRange[0], hlRange[1])
        self.decryptedbox.tag_configure("hl", background="light blue")

    def showLetterFrequencies(self):
        self.letterEntered("a")
        if len(self.ciphertextContents) == 0:
            return
        standardFrequencies = [8.17, 1.49, 2.78, 4.25, 12.70, 2.23, 2.02, 6.1, 6.97, 0.15, 0.77, 4.03, 2.41, 6.75, 7.51,
                               1.92, 0.1, 5.99, 6.34, 9.05, 2.76, 0.98, 2.36, 0.15, 1.97, 0.07]
        self.frequencyGraph.delete(ALL)
        # get letter frequencies first
        letterFrequencies = []
        for letter in range(26):
            letterFrequencies.append(self.ciphertextContents.count(chr(letter + 65)))
        maxFrequency = max(letterFrequencies)
        numLetters = sum(letterFrequencies)
        y = 300
        if numLetters == 0:
            return
        for letter in range(26):
            x = 10 + (letter * 16)
            height = letterFrequencies[letter] / maxFrequency * 290
            self.frequencyGraph.create_text(x, y, text=chr(letter + 65), anchor="n", font=("Arial", 12, "bold"))
            self.frequencyGraph.create_rectangle(x - 2, y - height, x + 3, y, fill="blue")
            self.frequencyGraph.create_text(x, y + 20, text=str(int(letterFrequencies[letter] / numLetters * 100)),
                                            fill="blue", anchor="n", font=("Arial", 9))
            self.frequencyGraph.create_text(x, y + 40, text=str(int(standardFrequencies[letter])), anchor="n",
                                            fill="red", font=("Arial", 9))
        self.frequencyGraph.create_text(10, y + 60, text="Frequencies in ciphertext (%)", anchor="nw", fill="blue",
                                        font=("Arial", 9))
        self.frequencyGraph.create_text(400, y + 60, text="Frequencies in English (%)", anchor="ne", fill="red",
                                        font=("Arial", 9))

    def showVowelTrowel(self):
        # calc most sociable letters
        self.letterEntered("e")
        letterArray = [[chr(x), set([])] for x in range(65, 91)]
        print(letterArray)
        for pos in range(len(self.ciphertextContents)):
            letterNum = ord(self.ciphertextContents[pos].upper())
            if letterNum >= 65 and letterNum <= 90:
                if pos > 0:
                    prev = ord(self.ciphertextContents[pos - 1].upper())
                    if prev >= 65 and prev <= 90:
                        letterArray[letterNum - 65][1].add(prev)
                if pos < len(self.ciphertextContents) - 1:
                    next = ord(self.ciphertextContents[pos + 1].upper())
                    if next >= 65 and next <= 90:
                        letterArray[letterNum - 65][1].add(next)

        # now sort
        for i in range(25):
            for j in range(25):
                if len(letterArray[j][1]) > len(letterArray[j + 1][1]):
                    letterArray[j], letterArray[j + 1] = letterArray[j + 1], letterArray[j]

        # now display
        self.frequencyGraph.delete(ALL)
        self.frequencyGraph.create_text(10, 10, text="The following are the most 'sociable' letters in the ciphertext.",
                                        anchor="nw", fill="blue", font=("Arial", 11))
        self.frequencyGraph.create_text(10, 30, text="(They appear alongside most other letters)",
                                        anchor="nw", fill="blue", font=("Arial", 11))
        self.frequencyGraph.create_text(10, 50, text="This means they are probably vowels.",
                                        anchor="nw", fill="blue", font=("Arial", 11))
        y = 80
        for letter in range(1, 10):
            char = letterArray[-letter][0]
            freq = len(letterArray[-letter][1])
            self.frequencyGraph.create_text(50, y + (letter * 30), text=char + " : " + str(freq),
                                            anchor="nw", fill="blue", font=("Courier", 12, "bold"))



    def checkentries(self,a,c,b):
        newmappings = [mapping.get() for mapping in self.mappings]
        # turn all uppercase:
        for mapNo in range(len(self.mappings)):
            thisletter = self.mappings[mapNo].get()
            if thisletter.islower():
                self.mappings[mapNo].set(thisletter.upper()) 
        # get rid of non -letters
        for mapNo in range(len(self.mappings)):
            thisletter = self.mappings[mapNo].get()
            if not thisletter.isalpha() and thisletter != "":
                self.mappings[mapNo].set("")

        # cut down to one letter
        for mapNo in range(len(self.mappings)):
            thisletter = self.mappings[mapNo].get()        
            if len(thisletter)>1:
                self.mappings[mapNo].set(thisletter[0])
        # cut out repetitions
        newmappings = [mapping.get() for mapping in self.mappings]
        oldmappings = [mapping for mapping in self.oldMappings]
        for mapNo in range(len(self.mappings)):
            thisletter = self.mappings[mapNo].get()                
            if newmappings.count(thisletter) >1 and oldmappings[mapNo] != thisletter:
                self.mappings[mapNo].set("")

        self.oldMappings = [mapping.get() for mapping in self.mappings]
        self.letterEntered(a)
        return True
    
    def letterEntered(self, event):
        #the top text box has been changed, so update the decrypted box
        self.ciphertextContents = self.entryBox.get(1.0, END)
        self.ciphertextContents = self.ciphertextContents.upper()
        self.ciphertextContents = self.ciphertextContents.replace("\n", "")
        plaintext = ""
        for letter in self.ciphertextContents:
            letterNum = ord(letter)-65
            if letterNum == 32 - 65:
                plaintext += " "
            elif letterNum>=0 and letterNum <=26:
                if self.mappings[letterNum].get() == "":
                    plaintext += "*"
                else:
                    plaintext += self.mappings[letterNum].get()
        self.decryptedbox.delete(1.0,END)
        self.decryptedbox.insert(1.0, plaintext)
        
        
    def randomKey(self):
        self.clearKey()
        letters = [chr(x) for x in range(65,91)]
        random.shuffle(letters)
        for x in range(26):
            self.mappings[x].set(letters[x])
            
    def clearKey(self):
        # clear old mappings
        for x in range(26):
            self.mappings[x].set("")


root=Tk()
root.title("Random Substitution Cipher Cracker")
root.resizable(width=False, height=False)
app = App(root)
root.mainloop()
print("Quit")

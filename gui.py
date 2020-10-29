from tkinter import *
import tweet


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.e2 = Entry()
        self.e1 = Entry()
        self.master = master
        self.init_window()
        textFile = open("score.txt", "r")
        self.score = textFile.read()
        textFile.close()

    def init_window(self):

        self.master.title("Tweet")

        Label(text="Name").grid(row=1)
        Label(text="Twitter Handle @").grid(row=2)
        Label(text="Defaults handle @realDonaldTrump").grid(row=4, column=1)

        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        Button(text="Tweet", command=self.tweet).grid(row=3, column=0)
        Button(text="Exit", command=exit).grid(row=3, column=1)

    def tweet(self):
        if self.e2.get() == "":
            self.e2 = "realDonaldTrump"
        else:
            self.e2 = self.e2.get()
        self.e2 = "@" + self.e2
        try:
            tweet.status(str(self.e2) + " " + str(self.e1.get()) + " got a score of:  " + self.score)
            print("Tweeted")

        except:
            print("You have no connection, idjut")


        self.exit()

    def exit(self):
        quit()

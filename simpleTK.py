from Tkinter import *
import test
class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"

    def createWidgets(self):
        self.QUIT = Label(self)
        self.QUIT["text"] = "MD"
        self.QUIT["fg"]   = "red"
        self.QUIT.pack({"side": "left"})


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()

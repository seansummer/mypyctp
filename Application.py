from Tkinter import *
from ctp import ApiStruct, MdApi, TraderApi
import MApi

class Application(Frame, MApi):
    def say_hi(self):
        print "hi there, everyone!"

    def createWidgets(self):        
        self.md = Label(self)
        self.md["text"] = "this is lable"
        self.md.pack({"side": "left"})
        self.md.bind(func=MdApi.OnRtnDepthMarketData)
        
    def OnRtnDepthMarketData(self, pDepthMarketData):
        self.md["text"]= pDepthMarketData

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.MD = MdApi('1007', '00000581', '123456', ['cu1309'])
        self.MD.RegisterFront('tcp://27.115.78.150:26213')
        self.MD.Init()
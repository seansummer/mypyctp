# -*- coding: utf-8 -*-

import time
from ctp import ApiStruct, MdApi, TraderApi
from Tkinter import *

class MyMdApi(MdApi):
    def __init__(self, brokerID, userID, password, instrumentIDs):
        self.requestID = 0
        self.brokerID = brokerID
        self.userID = userID
        self.password = password
        self.instrumentIDs = instrumentIDs
        self.Create()

    def Create(self):
        MdApi.Create(self)

    def RegisterFront(self, front):
        if isinstance(front, bytes):
            return MdApi.RegisterFront(self, front)
        for front in front:
            MdApi.RegisterFront(self, front)

    def OnFrontConnected(self):
        print('OnFrontConnected: Login...')
        req = ApiStruct.ReqUserLogin(
            BrokerID=self.brokerID, UserID=self.userID, Password=self.password)
        self.requestID += 1
        self.ReqUserLogin(req, self.requestID)

    def OnFrontDisconnected(self, nReason):
        print('OnFrontDisconnected:', nReason)

    def OnHeartBeatWarning(self, nTimeLapse):
        print('OnHeartBeatWarning:', nTimeLapse)

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        print('OnRspUserLogin:', pRspInfo)
        if pRspInfo.ErrorID == 0: # Success
            print('GetTradingDay:', self.GetTradingDay())
            self.SubscribeMarketData(self.instrumentIDs)

    def OnRspSubMarketData(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
        print('OnRspSubMarketData:', pRspInfo)

    def OnRspUnSubMarketData(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
        print('OnRspUnSubMarketData:', pRspInfo)

    def OnRspError(self, pRspInfo, nRequestID, bIsLast):
        print('OnRspError:', pRspInfo)

    def OnRspUserLogout(self, pUserLogout, pRspInfo, nRequestID, bIsLast):
        print('OnRspUserLogout:', pRspInfo)

    def OnRtnDepthMarketData(self, pDepthMarketData):
        d = pDepthMarketData
        print(d.TradingDay, d.InstrumentID, d.LastPrice, d.HighestPrice, d.LowestPrice, d.Volume, d.OpenInterest, d.UpdateTime, d.UpdateMillisec, d.AveragePrice)
        f = open('mdlog.txt','a')
        f.write(str(d)+'\n')
        f.close()
        return d

def main():
    mdapi = MyMdApi(b'1007', b'00000581', b'123456', [b'cu1309'])
    mdapi.RegisterFront(b'tcp://27.115.78.150:26213')
    mdapi.Init()
    return mdapi

class Application(Frame):
    def createWidgets(self):
        self.QUIT = Label(self, name="mdl")
        self.QUIT["text"] = "行情"
        self.QUIT["fg"]   = "red"
        self.QUIT.pack({"side": "left"})

if __name__ == '__main__':
    md = main()
    root = Tk()
    app = Application(master=root)
    app.mdl["text"] = md
    app.mainloop()
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

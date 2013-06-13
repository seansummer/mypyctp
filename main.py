# -*- coding: utf-8 -*-
import TApi, MApi, time, ConfigParser, Tkinter
from Tkinter import *

class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})
        
        self.md = Label(self)
        self.md["text"] = "this is lable"
        self.md.pack({"side": "left"})
        
        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

def connect():
    config = ConfigParser.ConfigParser()
    config.readfp(open('./config/config.cfg'))
    traderapi = TApi.MyTraderApi(config.get('ACCOUNT', 'BrokerID'), config.get('ACCOUNT', 'UserID'), config.get('ACCOUNT', 'Password'))
    traderapi.SubscribePublicTopic(0)
    traderapi.SubscribePrivateTopic(0)
    traderapi.RegisterFront(config.get('SERVER', 'TServerIP'))
    traderapi.Init()
    return traderapi

def main():
    menu = ['0 结算单确认','1 查询合约行情', '2 查询资金', '3 报单查询','4 成交查询', '5 持仓查询', '6 合约下单', '7 撤所有单','8 结算单查询','99 创建合约行情接收']
    t = connect()
    menucomm = {'0':t.ReqSettlementInfoConfirm,
                '1':t.ReqQryDepthMarketData,
                '2':t.ReqQryTradingAccount,
                '3':t.ReqQryOrder,
                '4':t.ReqQryTrade,
                '5':t.ReqQryInvestorPositionDetail,
                '6':t.ReqOrderInsert,
                '7':t.ReqOrderAction,
                '8':t.ReqQrySettlementInfo,
                #'99':MApi.mdconnect,
                }
    time.sleep(3)
    comm = ''
    while True:
        comm = raw_input('请输入命令序号,输入m显示菜单:')
        if str(comm) == 'm':
            for view in menu:
                print view
        elif str(comm) == 'x':
            print "退出程序"
            break
        if str(comm) in menucomm.keys():
            menucomm[str(comm)]()
        else:
            continue
        time.sleep(1)

if __name__ == '__main__':
    '''root = Tk()
    app = Application(master=root)
    mds = MApi.mdconnect()
    app.md["text"] = mds
    app.mainloop()
    root.destroy()'''
    try:
        main()
    except KeyboardInterrupt:
        print '终止程序'

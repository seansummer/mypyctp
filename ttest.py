# -*- coding: utf-8 -*-

import hashlib, os, sys, tempfile, time
from ctp import ApiStruct, MdApi, TraderApi

class MyTraderApi(TraderApi):
    #初始化交易API
    def __init__(self, brokerID, userID, password, instrumentIDs):
        self.requestID = 0
        self.brokerID = brokerID
        self.userID = userID
        self.password = password
        self.instrumentIDs = instrumentIDs
        self.Create()

    def Create(self):
        TraderApi.Create(self)

    def RegisterFront(self, front):
        if isinstance(front, bytes):
            return TraderApi.RegisterFront(self, front)
        for front in front:
            TraderApi.RegisterFront(self, front)

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
            #traderapi.ReqQryTradingAccount()
            #self.SubscribeMarketData(self.instrumentIDs)

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

    def OnRspQryOrder(self, pOrder, pRspInfo, nRequestID, bIsLast):
        print('OnRspQryOrder:', pOrder, pRspInfo)

    def OnRspQryTradingAccount(self, pTradingAccount, pRspInfo, nRequestID, bIsLast):
        print('OnRspQryTradingAccount:', pTradingAccount, pRspInfo)

    def ReqQryTradingAccount(self):
        #print self.brokerID, self.userID
        req = ApiStruct.QryTradingAccount(BrokerID=self.brokerID, InvestorID=self.userID)
        self.requestID += 1
        TraderApi.ReqQryTradingAccount(self, req, self.requestID)

    def ReqOrderInsert(self):
        print("start trade...")
        req = ApiStruct.InputOrder(BrokerID=self.brokerID, InvestorID=self.userID, InstrumentID=b'cu1309', UserID=self.userID, OrderPriceType='2', Direction='0', CombOffsetFlag='0', CombHedgeFlag='1', LimitPrice=52400, VolumeTotalOriginal=1, TimeCondition='3', VolumeCondition='1', MinVolume=0, ContingentCondition='1', StopPrice=0.0, ForceCloseReason='0', IsAutoSuspend=0 )
        self.requestID += 1
        TraderApi.ReqOrderInsert(self, req, self.requestID)

    def OnRtnOrder(self, pOrder):
        print('OnRtnOrder:', pOrder)

    def OnRspOrderInsert(self, pInputOrder, pRspInfo, nRequestID, bIsLast):
        print('OnRspOrderInsert:', pInputOrder, pRspInfo)

    def OnErrRtnOrderInsert(self, pInputOrder, pRspInfo):
        print('OnErrRtnOrderInsert:', pInputOrder, pRspInfo)

    def ReqSettlementInfoConfirm(self):
        req = ApiStruct.SettlementInfoConfirm(BrokerID=self.brokerID, InvestorID=self.userID, ConfirmDate=b'20130517', ConfirmTime=b'080000')
        self.requestID += 1
        answer = TraderApi.ReqSettlementInfoConfirm(self, req, self.requestID)
        print 'Confirm the SettlementInfo...' if answer == 0 else 'error on SettlementInfo'

def main():
    traderapi = MyTraderApi(b'1007', b'00000581', b'123456', [b'cu1309'])
    traderapi.SubscribePublicTopic(0)
    traderapi.SubscribePrivateTopic(0)
    traderapi.RegisterFront(b'tcp://27.115.78.150:26205')
    traderapi.Init()
    return traderapi

if __name__ == '__main__':
    r = main()
    try:
        while 1:
            print "ready..."
            #r.ReqSettlementInfoConfirm()
            r.ReqOrderInsert()
            r.ReqQryTradingAccount()
            time.sleep(10)
    except KeyboardInterrupt:
        pass

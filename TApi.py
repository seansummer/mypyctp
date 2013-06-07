# -*- coding: utf-8 -*-

import hashlib, os, sys, tempfile, time
from ctp import ApiStruct, MdApi, TraderApi
from xml.etree import ElementTree as ET

class MyTraderApi(TraderApi):
    #初始化交易API
    def __init__(self, brokerID, userID, password):
        self.requestID = 0
        self.brokerID = brokerID
        self.userID = userID
        self.password = password
        #self.instrumentIDs = instrumentIDs
        self.Create()

    def Create(self):
        TraderApi.Create(self)
        
    def FindErrors(self, value):
        tree = ET.parse('error.xml')
        root = tree.getroot()
        p = root.findall("error")
        for o in p:
            if o.attrib['value'] == str(value):
                print o.attrib['prompt']

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
        #print('OnRspQryOrder:', pOrder, pRspInfo)
        data = pOrder
        print('合约：%s|前置：%s|会话：%s|报单参考：%s|交易所：%s|系统报单号：%s' % (data.InstrumentID,data.FrontID,data.SessionID,data.OrderRef,data.ExchangeID,data.OrderSysID))

    def OnRspQryTradingAccount(self, pTradingAccount, pRspInfo, nRequestID, bIsLast):
        #print('OnRspQryTradingAccount:', pTradingAccount, pRspInfo)
        d = pTradingAccount
        print('投资者帐号:%s\n冻结的保证金:%.2f\n当前保证金总额:%.2f\n平仓盈亏:%.2f\n持仓盈亏:%.2f\n可用资金:%.2f\n可取资金:%.2f\n交易日:%s' % (d.AccountID, d.FrozenMargin, d.CurrMargin, d.CloseProfit, d.PositionProfit, d.Available, d.WithdrawQuota, d.TradingDay))

    def OnRspOrderInsert(self, pInputOrder, pRspInfo, nRequestID, bIsLast):
        print('OnRspOrderInsert:', pInputOrder, pRspInfo)

    def OnErrRtnOrderInsert(self, pInputOrder, pRspInfo):
        print('OnErrRtnOrderInsert:', pInputOrder, pRspInfo)

    def OnRspUserPasswordUpdate(self, pUserPasswordUpdate, pRspInfo, nRequestID, bIsLast):
        print('OnRspUserPasswordUpdate:', pUserPasswordUpdate, pRspInfo)

    def OnRspTradingAccountPasswordUpdate(self, pTradingAccountPasswordUpdate, pRspInfo, nRequestID, bIsLast):
        print('OnRspTradingAccountPasswordUpdate:', pTradingAccountPasswordUpdate, pRspInfo)

    def OnRspOrderAction(self, pOrderAction, pRspInfo, nRequestID, bIsLast):
        print('OnRspOrderAction:', pOrderAction, pRspInfo)

    def OnRspQueryMaxOrderVolume(self, pQueryMaxOrderVolume, pRspInfo, nRequestID, bIsLast):
        print('OnRspQueryMaxOrderVolume:', pQueryMaxOrderVolume, pRspInfo)

    def OnRspSettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
        print('OnRspSettlementInfoConfirm:', pSettlementInfoConfirm, pRspInfo)

    def OnRspTransferBankToFuture(self, pTransferBankToFutureRsp, pRspInfo, nRequestID, bIsLast):
        print('OnRspTransferBankToFuture:', pTransferBankToFutureRsp, pRspInfo)

    def OnRspTransferFutureToBank(self, pTransferFutureToBankRsp, pRspInfo, nRequestID, bIsLast):
        print('OnRspTransferFutureToBank:', pTransferFutureToBankRsp, pRspInfo)

    def OnRspTransferQryBank(self, pTransferQryBankRsp, pRspInfo, nRequestID, bIsLast):
        print('OnRspTransferQryBank:', pTransferQryBankRsp, pRspInfo)

    def OnRspTransferQryDetail(self, pTransferQryDetailRsp, pRspInfo, nRequestID, bIsLast):
        print('OnRspTransferQryDetail:', pTransferQryDetailRsp, pRspInfo)

    def OnRspQryTrade(self, pTrade, pRspInfo, nRequestID, bIsLast):
        print('OnRspQryTrade:', pTrade, pRspInfo)
        self.FindErrors(pRspInfo.ErrorID)

    def OnRspQryInvestor(self, pInvestor, pRspInfo, nRequestID, bIsLast):
        print('OnRspQryInvestor:', pInvestor, pRspInfo)

    def OnRspQryInvestorPosition(self, pInvestorPostion, pRspInfo, nRequestID, bIsLast):
        print('OnRspQryInvestorPosition:', pInvestorPostion, pRspInfo)

    def OnRspQryTradingCode(self, pTradingCode, pRspInfo, nReqestID, bIsLast):
        print('OnRspQryTradingCode:', pTradingCode, pRspInfo)

    def OnRspQryExchange(self, pExchange, pRspInfo, nRequset, bIsLast):
        print('OnRspQryExchange:', pExchange, pRspInfo)

    def OnRspQryDepthMarketData(self, pDepthMarketData, pRspInfo, nRequset, bIsLast):
        d = pDepthMarketData
        print('OnRspQryDepthMarketData:')
        print("合约:%s\n最新价:%.2f\n最高价:%.2f\n最低价:%.2f\n数量:%d\n最后修改时间:%s\n买价:%.2f\n买量:%d\n卖价:%.2f\n卖量:%d" % (d.InstrumentID,d.LastPrice,d.HighestPrice,d.LowestPrice,d.Volume,d.UpdateTime,d.BidPrice1,d.BidVolume1,d.AskPrice1,d.AskVolume1))
        self.FindErrors(pRspInfo.ErrorID)

    def OnRspQrySettlementInfo(self, pSettlementInfo, pRspInfo, nRequset, bIsLast):
        print('OnRspQrySettlementInfo:', pSettlementInfo, pRspInfo)

    def OnRspQryTransferBank(self, pTransferBank, pRspInfo, nRequset, bIsLast):
        print('OnRspQryTransferBank:', pTransferBank, pRspInfo)

    def OnRspQryInvestorPositionDetail(self, pInvestorPositionDetail, pRspInfo, nRequestID, bIsLast):
        print('OnRspQryInvestorPositionDetail',pInvestorPositionDetail, pRspInfo)

    def OnRspQryNotice(self, pNotice, pRspInfo, nRequestID, bIsLast):
        print('OnRspQryNotice:', pNotice, pRspInfo)

    def OnRspQryInstrument(self, pInstrument, pRspInfo, nRequestID, bIsLast):
        print('OnRspQryInstrument:', pInstrument, pRspInfo)

    def OnRtnTrade(self, pTrade):
        print('OnRtnTrade:', pTrade)

    def OnRtnOrder(self, pOrder):
        print('OnRtnOrder:', pOrder)

    def OnErrRtnOrderAction(self, pOrderAction, pRspInfo):
        print('OnErrRtnOrderAction:', pOrderAction, pRspInfo)
        
    def OnRspQrySettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
        print('OnRspQrySettlementInfoConfirm:', pSettlementInfoConfirm, pRspInfo)

    def OnRspQryContractBank(self, pContractBank, pRspInfo, nRequestID, bIsLast):
        print('OnRspQryContractBank:', pContractBank, pRspInfo)

    def ReqUserPasswordUpdate(self, oldpass, newpass):
        req = ApiStruct.UserPasswordUpdate(BrokerID=self.brokerID, InvestorID=self.userID, OldPassword=oldpass, NewPassword=newpass)
        self.requestID += 1
        answer = TraderApi.ReqUserPasswordUpdate(self, req, self.requestID)
        print('UserPasswordUpdate...') if answer == 0 else 'error on UserPasswordUpdate'

    def ReqQryDepthMarketData(self):
        pInstrumentID = raw_input('输入合约名称:')
        req = ApiStruct.QryDepthMarketData(InstrumentID=pInstrumentID)
        self.requestID += 1
        answer = TraderApi.ReqQryDepthMarketData(self, req, self.requestID)
        print('ReqQryDepthMarketData...') if answer ==0 else 'error on ReqQryDepthMarketData'

    def ReqQryInvestorPositionDetail(self):
        req = ApiStruct.QryInvestorPositionDetail(BrokerID=self.brokerID, InvestorID=self.userID)
        self.requestID += 1
        answer = TraderApi.ReqQryInvestorPositionDetail(self, req, self.requestID)
        print('ReqQryInvestorPositionDetail...') if answer ==0 else 'error on ReqQryInvestorPositionDetail'

    def ReqQryTradingAccount(self):
        #print self.brokerID, self.userID
        req = ApiStruct.QryTradingAccount(BrokerID=self.brokerID, InvestorID=self.userID)
        self.requestID += 1
        TraderApi.ReqQryTradingAccount(self, req, self.requestID)

    def ReqOrderInsert(self):
        instrumentid = raw_input('请输入合约号:')
        orderpricetype = raw_input('任意价1 限价2 最优价3 最新价4:')
        direction = raw_input('买1 卖2:')
        limitprice = input('价格：')
        volumetotaloriginal = raw_input('数量:')
        req = ApiStruct.InputOrder(BrokerID=self.brokerID, InvestorID=self.userID, InstrumentID=instrumentid, UserID=self.userID, OrderPriceType=str(orderpricetype), Direction=str(direction), CombOffsetFlag='0', CombHedgeFlag='1', LimitPrice=float(limitprice), VolumeTotalOriginal=int(volumetotaloriginal), TimeCondition='3', VolumeCondition='1', MinVolume=0, ContingentCondition='1', StopPrice=0.0, ForceCloseReason='0', IsAutoSuspend=0 )
        self.requestID += 1
        TraderApi.ReqOrderInsert(self, req, self.requestID)

    def ReqQryOrder(self):
        req = ApiStruct.QryOrder(BrokerID=self.brokerID, InvestorID=self.userID)
        self.requestID += 1
        TraderApi.ReqQryOrder(self, req, self.requestID)

    def ReqQryTrade(self):
        req = ApiStruct.QryTrade(BrokerID=self.brokerID, InvestorID=self.userID)
        self.requestID += 1
        TraderApi.ReqQryTrade(self, req, self.requestID)

    def ReqSettlementInfoConfirm(self):
        req = ApiStruct.SettlementInfoConfirm(BrokerID=self.brokerID, InvestorID=self.userID)
        self.requestID += 1
        answer = TraderApi.ReqSettlementInfoConfirm(self, req, self.requestID)
        if answer == 0:
            print '结算单确认成功'
        else:
            '结算单确认错误'
        
    def ReqOrderAction(self):
        ordersysid = raw_input("请输入系统报单号：")
        req = ApiStruct.Order(BrokerID=self.brokerID,UserID=self.userID,OrderSysID=ordersysid)
        self.requestID += 1
        answer = TraderApi.ReqOrderAction(self, req, self.requestID)
        if answer == 0:
            print "撤单请求发送成功"
        pass
        
        



if __name__ == '__main__':
    #r = main()
    try:
        while 1:
            print "ready..."
            #r.ReqSettlementInfoConfirm()
            #r.ReqOrderInsert()
            #r.ReqQryTradingAccount()
            #r.ReqQryDepthMarketData(b'cu1309')
            #r.ReqQryInvestorPositionDetail()
            time.sleep(10)
    except KeyboardInterrupt:
        pass

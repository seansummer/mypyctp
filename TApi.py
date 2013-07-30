# -*- coding: utf-8 -*-

import hashlib, os, sys, tempfile, time, logging, ConfigParser
from ctp import ApiStruct, MdApi, TraderApi
from xml.etree import ElementTree as ET

class MyTraderApi(TraderApi):
    FORMAT= '%(name)s %(levelname)s %(asctime)s %(process)d %(processName)s %(thread)d %(threadName)s %(message)s'
    logging.basicConfig(filename='./log/' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + 'tradelog.log', filemode='a', level=logging.DEBUG, format=FORMAT)
    orderStatus = {'0':'全部成交',
                   '1':'部分成交还在队列中',
                   '2':'部分成交不在队列中',
                   '3':'未成交还在队列中',
                   '4':'未成交不在队列中',
                   '5':'撤单',
                   'a':'未知',
                   'b':'尚未'}
    #初始化交易API
    def __init__(self, brokerID, userID, password):
        self.requestID = 0
        self.brokerID = brokerID
        self.userID = userID
        self.password = password
        self.instrumentIDs = 'cu1311'
        self.investorPosition = []
        self.investorPositionDetail = []
        self.qryOrder = []
        self.Create()

    def Create(self):
        TraderApi.Create(self)
        
    def FindErrors(self, value):
        tree = ET.parse('error.xml')
        root = tree.getroot()
        p = root.findall("error")
        for o in p:
            if o.attrib['value'] == str(value):
                logging.error(o.attrib['prompt'])

    def RegisterFront(self, front):
        if isinstance(front, bytes):
            return TraderApi.RegisterFront(self, front)
        for front in front:
            TraderApi.RegisterFront(self, front)

    def OnFrontConnected(self):
        logging.info('OnFrontConnected: Login...')
        req = ApiStruct.ReqUserLogin(BrokerID=self.brokerID, UserID=self.userID, Password=self.password)
        self.requestID += 1
        self.ReqUserLogin(req, self.requestID)

    def OnFrontDisconnected(self, nReason):
        logging.info('OnFrontDisconnected:' + str(nReason))

    def OnHeartBeatWarning(self, nTimeLapse):
        logging.info('OnHeartBeatWarning:' + str(nTimeLapse))

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        logging.info('OnRspUserLogin:' + str(self.FindErrors(pRspInfo.ErrorID)))
        if pRspInfo.ErrorID == 0: # Success
            logging.info('GetTradingDay:' + str(self.GetTradingDay()))

    def OnRspSubMarketData(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
        logging.info('OnRspSubMarketData:'+ str(pRspInfo))

    def OnRspUnSubMarketData(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
        logging.info('OnRspUnSubMarketData:' + str(pRspInfo))

    def OnRspError(self, pRspInfo, nRequestID, bIsLast):
        logging.error('OnRspError:' + str(pRspInfo))

    def OnRspUserLogout(self, pUserLogout, pRspInfo, nRequestID, bIsLast):
        logging.info('OnRspUserLogout:' + str(pRspInfo))

    def OnRtnDepthMarketData(self, pDepthMarketData):
        d = pDepthMarketData
        print d.TradingDay, d.InstrumentID, d.LastPrice, d.HighestPrice, d.LowestPrice, d.Volume, d.OpenInterest, d.UpdateTime, d.UpdateMillisec, d.AveragePrice

    def OnRspQryOrder(self, pOrder, pRspInfo, nRequestID, bIsLast):
        #print('OnRspQryOrder:', pOrder, pRspInfo)
        data = pOrder
        #print '合约：%s|前置：%s|会话：%s|交易所：%s|系统报单号：%s|报单状态：%s|委托时间:%s' % (data.InstrumentID,data.FrontID,data.SessionID,data.ExchangeID,data.OrderSysID,self.orderStatus[data.OrderStatus],data.InsertTime)
        if data == None:
            print "没有报单"
        elif data.OrderStatus == '3':
            self.qryOrder.append([data.InstrumentID,data.FrontID,data.SessionID,data.ExchangeID,data.OrderSysID,data.InsertTime])

    def OnRspQryTradingAccount(self, pTradingAccount, pRspInfo, nRequestID, bIsLast):
        #print('OnRspQryTradingAccount:', pTradingAccount, pRspInfo)
        d = pTradingAccount
        print '投资者帐号:%s\n冻结的保证金:%.2f\n当前保证金总额:%.2f\n平仓盈亏:%.2f\n持仓盈亏:%.2f\n可用资金:%.2f\n可取资金:%.2f\n交易日:%s' % (d.AccountID, d.FrozenMargin, d.CurrMargin, d.CloseProfit, d.PositionProfit, d.Available, d.WithdrawQuota, d.TradingDay)

    def OnRspOrderInsert(self, pInputOrder, pRspInfo, nRequestID, bIsLast):
        logging.info('OnRspOrderInsert:' + str(pInputOrder) + str(pRspInfo))

    def OnErrRtnOrderInsert(self, pInputOrder, pRspInfo):
        logging.error('OnErrRtnOrderInsert:'+ str(pInputOrder) + str(self.FindErrors(pRspInfo.ErrorID)))

    def OnRspUserPasswordUpdate(self, pUserPasswordUpdate, pRspInfo, nRequestID, bIsLast):
        print 'OnRspUserPasswordUpdate:', pUserPasswordUpdate, pRspInfo

    def OnRspTradingAccountPasswordUpdate(self, pTradingAccountPasswordUpdate, pRspInfo, nRequestID, bIsLast):
        print 'OnRspTradingAccountPasswordUpdate:', pTradingAccountPasswordUpdate, pRspInfo

    def OnRspOrderAction(self, pOrderAction, pRspInfo, nRequestID, bIsLast):
        logging.info('OnRspOrderAction:' + str(pOrderAction) + str(self.FindErrors(pRspInfo.ErrorID)))

    def OnRspQueryMaxOrderVolume(self, pQueryMaxOrderVolume, pRspInfo, nRequestID, bIsLast):
        print 'OnRspQueryMaxOrderVolume:', pQueryMaxOrderVolume, pRspInfo

    def OnRspSettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
        print 'OnRspSettlementInfoConfirm:', pSettlementInfoConfirm, self.FindErrors(pRspInfo.ErrorID)

    def OnRspTransferBankToFuture(self, pTransferBankToFutureRsp, pRspInfo, nRequestID, bIsLast):
        print 'OnRspTransferBankToFuture:', pTransferBankToFutureRsp, pRspInfo

    def OnRspTransferFutureToBank(self, pTransferFutureToBankRsp, pRspInfo, nRequestID, bIsLast):
        print 'OnRspTransferFutureToBank:', pTransferFutureToBankRsp, pRspInfo

    def OnRspTransferQryBank(self, pTransferQryBankRsp, pRspInfo, nRequestID, bIsLast):
        print 'OnRspTransferQryBank:', pTransferQryBankRsp, pRspInfo

    def OnRspTransferQryDetail(self, pTransferQryDetailRsp, pRspInfo, nRequestID, bIsLast):
        print 'OnRspTransferQryDetail:', pTransferQryDetailRsp, pRspInfo

    def OnRspQryTrade(self, pTrade, pRspInfo, nRequestID, bIsLast):
        #print 'OnRspQryTrade:', pTrade, pRspInfo
        data = pTrade
        print "合约：%s|交易所：%s|成交编号：%s|买卖：%s|系统编号：%s|成交类型：%s|成交价格：%s|数量：%s|成交时间：%s" % (data.InstrumentID,data.ExchangeID,data.TradeID,data.Direction,data.OrderSysID,data.OffsetFlag,data.Price,data.Volume,data.TradeTime)

    def OnRspQryInvestor(self, pInvestor, pRspInfo, nRequestID, bIsLast):
        logging.info('OnRspQryInvestor:', pInvestor, self.FindErrors(pRspInfo.ErrorID))

    def OnRspQryInvestorPosition(self, pInvestorPosition, pRspInfo, nRequestID, bIsLast):
        #print 'OnRspQryInvestorPosition:', pInvestorPostion, pRspInfo
        data = pInvestorPosition
        #print 'OnRspQryInvestorPostion', data
        #print '合约：%s|买卖：%s|手数：%s|开仓价：%s|保证金：%s|持仓盈亏：%s' % (data.InstrumentID, data.PosiDirection, data.OpenVolume, data.OpenAmount, data.UseMargin, data.PositionProfit)
        if bIsLast == 0:
            self.investorPosition = []
        if data == None:
            print '没有持仓'
        else:
            #print data
            self.investorPosition.append([data.InstrumentID, data.PosiDirection, data.Position, data.OpenAmount, data.UseMargin, data.PositionProfit] )
        
    def OnRspQryTradingCode(self, pTradingCode, pRspInfo, nReqestID, bIsLast):
        print 'OnRspQryTradingCode:', pTradingCode, pRspInfo

    def OnRspQryExchange(self, pExchange, pRspInfo, nRequset, bIsLast):
        print 'OnRspQryExchange:', pExchange, pRspInfo

    def OnRspQryDepthMarketData(self, pDepthMarketData, pRspInfo, nRequset, bIsLast):
        d = pDepthMarketData
        for o in str(d).split(','):
            print o            
        print 'OnRspQryDepthMarketData:'
        print "合约:%s\n最新价:%.2f\n最高价:%.2f\n最低价:%.2f\n数量:%d\n最后修改时间:%s\n买价:%.2f\n买量:%d\n卖价:%.2f\n卖量:%d" % (d.InstrumentID,d.LastPrice,d.HighestPrice,d.LowestPrice,d.Volume,d.UpdateTime,d.BidPrice1,d.BidVolume1,d.AskPrice1,d.AskVolume1)

    def OnRspQrySettlementInfo(self, pSettlementInfo, pRspInfo, nRequset, bIsLast):
        print 'OnRspQrySettlementInfo:', pSettlementInfo, pRspInfo
        for o in str(pSettlementInfo).split(','):
            print o

    def OnRspQryTransferBank(self, pTransferBank, pRspInfo, nRequset, bIsLast):
        print 'OnRspQryTransferBank:', pTransferBank, pRspInfo

    def OnRspQryInvestorPositionDetail(self, pInvestorPositionDetail, pRspInfo, nRequestID, bIsLast):
        #print 'OnRspQryInvestorPositionDetail',pInvestorPositionDetail, pRspInfo
        data = pInvestorPositionDetail
        if data == None:
            print '没有持仓'
        elif data.Volume > 0:
        #print data
        #print '成交编号：%s|合约：%s|买卖：%s|手数：%s|开仓价：%s|保证金：%s|持仓盈亏：%s|平仓盈亏：%s|交易所：%s' % (data.TradeID, data.InstrumentID, data.Direction, data.Volume, data.OpenPrice, data.Margin, data.PositionProfitByTrade, data.CloseProfitByDate, data.ExchangeID)
            self.investorPositionDetail.append([data.TradeID, data.InstrumentID, data.Direction, data.Volume, data.OpenPrice, data.ExchangeID])
        
    def OnRspQryNotice(self, pNotice, pRspInfo, nRequestID, bIsLast):
        print 'OnRspQryNotice:', pNotice, pRspInfo

    def OnRspQryInstrument(self, pInstrument, pRspInfo, nRequestID, bIsLast):
        print 'OnRspQryInstrument:', pInstrument, pRspInfo

    def OnRtnTrade(self, pTrade):
        #print 'OnRtnTrade:', pTrade
        logging.info('OnRtnTrade:' + str(pTrade))
        
    def OnRtnOrder(self, pOrder):
        #print 'OnRtnOrder:', pOrder
        #data = pOrder
        #print '报单编号：%s|合约：%s|买卖：%s|报单状态：%s|报价：%s|数量：%s|成交量：%s|剩余数量：%s|详细状态：%s|报单时间：%s|最后更新时间：%s|交易所：%s' % (data.OrderSysID,data.InstrumentID, data.Direction, data.OrderStatus, data.LimitPrice, data.VolumeTotalOriginal, data.VolumeTraded, data.VolumeTotal, str(data.StatusMsg).decode('gb2312'), data.InsertTime, data.UpdateTime, data.ExchangeID)
        logging.info('OnRtnOrder:' + str(pOrder))

    def OnErrRtnOrderAction(self, pOrderAction, pRspInfo):
        logging.error('OnErrRtnOrderAction:' + str(pOrderAction) + str(self.FindErrors(pRspInfo.ErrorID)))
        data = pOrderAction
        print str(data.StatusMsg).decode('gb2312')
        
    def OnRspQrySettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
        print 'OnRspQrySettlementInfoConfirm:', pSettlementInfoConfirm, self.FindErrors(pRspInfo.ErrorID)

    def OnRspQryContractBank(self, pContractBank, pRspInfo, nRequestID, bIsLast):
        print 'OnRspQryContractBank:', pContractBank, pRspInfo

    def ReqUserPasswordUpdate(self, oldpass, newpass):
        req = ApiStruct.UserPasswordUpdate(BrokerID=self.brokerID, InvestorID=self.userID, OldPassword=oldpass, NewPassword=newpass)
        self.requestID += 1
        answer = TraderApi.ReqUserPasswordUpdate(self, req, self.requestID)
        print 'UserPasswordUpdate...' if answer == 0 else 'error on UserPasswordUpdate'

    def ReqQryDepthMarketData(self):
        pInstrumentID = raw_input('输入合约名称:')
        req = ApiStruct.QryDepthMarketData(InstrumentID=pInstrumentID)
        self.requestID += 1
        answer = TraderApi.ReqQryDepthMarketData(self, req, self.requestID)
        print 'ReqQryDepthMarketData...' if answer ==0 else 'error on ReqQryDepthMarketData'
        
    def ReqQryInvestorPosition(self):
        req = ApiStruct.QryInvestorPosition(BrokerID=self.brokerID, InvestorID=self.userID)
        self.requestID += 1
        answer = TraderApi.ReqQryInvestorPosition(self, req, self.requestID)
        #print 'ReqQryInvestorPosition...' if answer ==0 else 'error on ReqQryInvestorPosition'

    def ReqQryInvestorPositionDetail(self):
        req = ApiStruct.QryInvestorPositionDetail(BrokerID=self.brokerID, InvestorID=self.userID)
        self.requestID += 1
        TraderApi.ReqQryInvestorPositionDetail(self, req, self.requestID)
        #print 'ReqQryInvestorPositionDetail...' if answer ==0 else 'error on ReqQryInvestorPositionDetail'

    def ReqQryTradingAccount(self):
        #print self.brokerID, self.userID
        req = ApiStruct.QryTradingAccount(BrokerID=self.brokerID, InvestorID=self.userID)
        self.requestID += 1
        TraderApi.ReqQryTradingAccount(self, req, self.requestID)

    def ReqOrderInsert(self, instrumentid, comboffsetflag, direction, limitprice, volumetotaloriginal = 1):
        #instrumentid = raw_input('请输入合约号:')
        #orderpricetype = raw_input('任意价1 限价2 最优价3 最新价4:')
        #comboffsetflag = raw_input('开仓0平仓1平今3平昨4：')
        #direction = raw_input('买0 卖1:')
        #limitprice = input('价格：')
        #volumetotaloriginal = raw_input('数量:')
        req = ApiStruct.InputOrder(BrokerID=self.brokerID, InvestorID=self.userID, InstrumentID=instrumentid, UserID=self.userID, OrderPriceType=str(2), Direction=str(direction), CombOffsetFlag=str(comboffsetflag), CombHedgeFlag='1', LimitPrice=float(limitprice), VolumeTotalOriginal=int(volumetotaloriginal), TimeCondition='3', VolumeCondition='1', MinVolume=0, ContingentCondition='1', StopPrice=0.0, ForceCloseReason='0', IsAutoSuspend=0 )
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
        
    def ReqOrderAction(self, ordersysid, exchangeid):
        #ordersysid = raw_input("请输入系统报单号：")
        #exchangeid = raw_input("请输入交易所SHFE/DCE/CFFE/CZCE：")
        #req = ApiStruct.OrderAction(InstrumentID=self.instrumentIDs, BrokerID=self.brokerID, InvestorID=self.userID, ActionFlag=b'0', FrontID=1, SessionID=865534192, OrderRef='           2', ExchangeID='SHFE', LimitPrice=52100.0, RequestID=65537, OrderSysID='     1036148')
        req = ApiStruct.OrderAction(BrokerID=self.brokerID, InvestorID=self.userID, ActionFlag=b'0', OrderSysID=str(ordersysid).rjust(12), ExchangeID=str(exchangeid).upper())
        self.requestID += 1
        TraderApi.ReqOrderAction(self, req, self.requestID)
    
    def ReqQrySettlementInfo(self):
        req = ApiStruct.SettlementInfo(BrokerID=self.brokerID,UserID=self.userID)
        self.requestID += 1
        answer = TraderApi.ReqQrySettlementInfo(self, req, self.requestID)
        if answer == 0:
            print "结算查询发送成功"
        pass
    
    #查询交易所
    def ReqQryExchange(self):
        req = ApiStruct.QryExchange(ExchageID = 'SHFE')
        self.requestID += 1
        TraderApi.ReqQryExchange(self, req, self.requestID)
        
def tconnect():
    config = ConfigParser.ConfigParser()
    config.readfp(open('./config/config.cfg'))
    traderapi = MyTraderApi(config.get('ACCOUNT', 'BrokerID'), config.get('ACCOUNT', 'UserID'), config.get('ACCOUNT', 'Password'))
    traderapi.SubscribePublicTopic(1)
    traderapi.SubscribePrivateTopic(1)
    traderapi.RegisterFront(config.get('SERVER', 'TServerIP'))
    traderapi.Init()
    return traderapi


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

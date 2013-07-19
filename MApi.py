# -*- coding: utf-8 -*-

import hashlib, os, sys, tempfile, time, ConfigParser, logging
from ctp import ApiStruct, MdApi, TraderApi   
        
class MyMdApi(MdApi):
    FORMAT= '%(name)s %(levelname)s %(asctime)s %(process)d %(processName)s %(thread)d %(threadName)s %(message)s'
    logging.basicConfig(filename='./log/' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + 'mdlog.log', filemode='a', level=logging.DEBUG, format=FORMAT)
#初始化MyMdApi类
    def __init__(self, brokerID, userID, password, instrumentIDs):
        self.requestID = 0
        self.brokerID = brokerID
        self.userID = userID
        self.password = password
        self.instrumentIDs = instrumentIDs
        self.Create()

#创建MdApi
#@param pszFlowPath 存贮订阅信息文件的目录，默认为当前目录
#@return 创建出的UserApi
#modify for udp marketdata
    def Create(self):
        MdApi.Create(self)

#注册前置机网络地址
#@param pszFrontAddress：前置机网络地址。
#@remark 网络地址的格式为：“protocol://ipaddress:port”，如：”tcp://127.0.0.1:17001”。
#@remark “tcp”代表传输协议，“127.0.0.1”代表服务器地址。”17001”代表服务器端口号。'''
    def RegisterFront(self, front):
        if isinstance(front, bytes):
            return MdApi.RegisterFront(self, front)
        for front in front:
            MdApi.RegisterFront(self, front)

#当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用。
    def OnFrontConnected(self):
        logging.info('OnFrontConnected: Connect...')
        req = ApiStruct.ReqUserLogin(BrokerID=self.brokerID, UserID=self.userID, Password=self.password)
        self.requestID += 1
        self.ReqUserLogin(req, self.requestID)

#当客户端与交易后台通信连接断开时，该方法被调用。当发生这个情况后，API会自动重新连接，客户端可不做处理。
#@param nReason 错误原因
#        0x1001 网络读失败
#        0x1002 网络写失败
#        0x2001 接收心跳超时
#        0x2002 发送心跳失败
#        0x2003 收到错误报文
    def OnFrontDisconnected(self, nReason):
        logging.info('OnFrontDisconnected:' + str(nReason))

#心跳超时警告。当长时间未收到报文时，该方法被调用。
#@param nTimeLapse 距离上次接收报文的时间
    def OnHeartBeatWarning(self, nTimeLapse):
        logging.info('OnHeartBeatWarning:' + str(nTimeLapse))

#登录请求响应
    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        logging.info('OnRspUserLogin:' + str(pRspInfo))
        if pRspInfo.ErrorID == 0: # Success
            logging.info('GetTradingDay:' + self.GetTradingDay())
            self.SubscribeMarketData(self.instrumentIDs)

#订阅行情应答
    def OnRspSubMarketData(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
        logging.info('OnRspSubMarketData:' + str(pRspInfo))

#退订行情应答
    def OnRspUnSubMarketData(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
        logging.info('OnRspUnSubMarketData:' + str(pRspInfo))

#错误应答
    def OnRspError(self, pRspInfo, nRequestID, bIsLast):
        logging.error('OnRspError:'+ str(pRspInfo))

#登出请求应答
    def OnRspUserLogout(self, pUserLogout, pRspInfo, nRequestID, bIsLast):
        logging.info('OnRspUserLogout:'+ str(pRspInfo))

#深度行情通知
    def OnRtnDepthMarketData(self, pDepthMarketData):
        data = pDepthMarketData
        #print('OnRspQryDepthMarketData:')
        datas = "{0:s}|{1:.2f}|{2:.2f}|{3:.2f}|{4:d}|{5:s}|{6:.2f}|{7:d}|{8:.2f}|{9:d}".format(data.InstrumentID,data.LastPrice,data.HighestPrice,data.LowestPrice,data.Volume,data.UpdateTime,data.BidPrice1,data.BidVolume1,data.AskPrice1,data.AskVolume1)
        #print("合约:%s\n最新价:%.2f\t最高价:%.2f\t最低价:%.2f\t数量:%d\t最后修改时间:%s\n买价:%.2f\t买量:%d\t卖价:%.2f\t卖量:%d" % (d.InstrumentID,d.LastPrice,d.HighestPrice,d.LowestPrice,d.Volume,d.UpdateTime,d.BidPrice1,d.BidVolume1,d.AskPrice1,d.AskVolume1))
        mdname = './log/' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + 'md.txt'
        f = open(mdname,'a')
        f.write(str(datas)+'\n')
        f.close()
        
def mdconnect():
    config = ConfigParser.ConfigParser()
    config.readfp(open('./config/config.cfg'))
    instrument = list()
    instrument.append(raw_input("请输入合约号:"))
    print instrument
    mdapi = MyMdApi(config.get('ACCOUNT', 'BrokerID'), config.get('ACCOUNT', 'UserID'), config.get('ACCOUNT', 'Password'), instrument)
    mdapi.RegisterFront(config.get('SERVER', 'MServerIP'))
    mdapi.Init()
    return mdapi
        
        
if __name__ == '__main__':
    md = mdconnect()
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

# -*- coding: utf-8 -*-

import time, ConfigParser, logging, MApi, linecache, TApi
from ctp import ApiStruct, MdApi, TraderApi   

def tconnect():
    config = ConfigParser.ConfigParser()
    config.readfp(open('./config/config.cfg'))
    traderapi = TApi.MyTraderApi(config.get('ACCOUNT', 'BrokerID'), config.get('ACCOUNT', 'UserID'), config.get('ACCOUNT', 'Password'))
    traderapi.SubscribePublicTopic(1)
    traderapi.SubscribePrivateTopic(1)
    traderapi.RegisterFront(config.get('SERVER', 'TServerIP'))
    traderapi.Init()
    return traderapi

def getlastmd():
    filename = './data/' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + 'cu1311' + '.txt'
    with open(filename, 'r') as f:
        linenum = len(f.readlines())
        last = linecache.getline(filename, linenum)
        linecache.clearcache()
        return last

def main():
    t = tconnect()
    time.sleep(3)
    while True:
        t.ReqQryInvestorPosition()
        time.sleep(3)
        md = getlastmd()
        price = md.split('|')[1]
        print t.investorPosition
        for v in t.investorPosition:
            if v[-1] >= 200 and v[1] == '2':
                t.ReqOrderInsert('cu1311', 3, 1, price, 1)
            elif v[-1] >= 200 and v[1] == '3':
                t.ReqOrderInsert('cu1311', 3, 0, price, 1)
        time.sleep(0.5)
    #print t.investorPosition




if __name__ == '__main__':
    main()
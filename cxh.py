# -*- coding: utf-8 -*-

import time, ConfigParser, logging, MApi, linecache, TApi
from ctp import ApiStruct, MdApi, TraderApi   

def tconnect():
    config = ConfigParser.ConfigParser()
    config.readfp(open('./config/config.cfg'))
    traderapi = TApi.MyTraderApi(config.get('ACCOUNT', 'BrokerID'), config.get('ACCOUNT', 'UserID'), config.get('ACCOUNT', 'Password'))
    traderapi.SubscribePublicTopic(0)
    traderapi.SubscribePrivateTopic(0)
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
        
def cxhactive(checknum, price):
    if checknum > 2:
        print "做多！"
        checknum = 1
    elif checknum < -1:
        print "做空"
        checknum = 1
    return checknum
        
def main():
    preprice = 0
    checknum = 0
    t = tconnect()
    while True:
        md = getlastmd()
        price = md.split('|')[1]
        if preprice < price:
            checknum = checknum + 1
        elif preprice > price:
            checknum = checknum - 1
        else:
            pass
        preprice = price
        print price,checknum
        if checknum > 2:
            t.ReqOrderInsert('cu1311', 0, 0, price, 1)
        elif checknum < -1:
            t.ReqOrderInsert('cu1311', 0, 1, price, 1)
        checknum = cxhactive(checknum, price)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
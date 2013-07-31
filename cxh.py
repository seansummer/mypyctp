# -*- coding: utf-8 -*-

import time, ConfigParser, logging, MApi, linecache, TApi
from ctp import ApiStruct, MdApi, TraderApi   

def getlastmd():
    config = ConfigParser.ConfigParser()
    config.readfp(open('./config/config.cfg'))
    filename = './data/' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + config.get('ACCOUNT', 'CXHInstrument') + '.txt'
    with open(filename, 'r') as f:
        linenum = len(f.readlines())
        last = linecache.getline(filename, linenum)
        linecache.clearcache()
        return last
        
def cxhactive(checknum, price):
    if checknum > 3:
        print "反向做空！"
        checknum = 1
    elif checknum < -2:
        print "反向做多！"
        checknum = 1
    return checknum
        
def main():
    preprice = 0
    checknum = 0
    pretime = ''
    t = TApi.tconnect()
    time.sleep(3)
    t.ReqSettlementInfoConfirm()
    while True:
        md = getlastmd()
        price = md.split('|')[1]
        if md.split('|')[5] + md.split('|')[6] <> pretime:
            if preprice < price:
                checknum = checknum + 1
            elif preprice > price:
                checknum = checknum - 1
            else:
                pass
            preprice = price
            print price,checknum,pretime
            if checknum > 3:
                t.ReqOrderInsert('cu1311', 0, 1, price, 1)
            elif checknum < -2:
                t.ReqOrderInsert('cu1311', 0, 0, price, 1)
            checknum = cxhactive(checknum, price)
        pretime = md.split('|')[5] + md.split('|')[6]
        time.sleep(0.5)

if __name__ == '__main__':
    main()
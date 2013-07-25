# -*- coding: utf-8 -*-

import time, ConfigParser, logging, MApi, linecache, TApi
from ctp import ApiStruct, MdApi, TraderApi   

def getlastmd():
    filename = './data/' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + 'cu1311' + '.txt'
    with open(filename, 'r') as f:
        linenum = len(f.readlines())
        last = linecache.getline(filename, linenum)
        linecache.clearcache()
        return last

def main():
    t = TApi.tconnect()
    time.sleep(3)
    while True:
        t.ReqQryInvestorPosition()
        time.sleep(2)
        md = getlastmd()
        price = md.split('|')[1]
        buyprice = md.split('|')[-4]
        sellprice = md.split('|')[-2]
        if t.investorPosition <> []:
            print t.investorPosition
            for v in t.investorPosition:
            #v[1] 2多头 3空头
                if v[-1] >= 200 and v[1] == '2':
                    t.ReqOrderInsert('cu1311', 3, 1, sellprice, 1)
                elif v[-1] >= 200 and v[1] == '3':
                    t.ReqOrderInsert('cu1311', 3, 0, buyprice, 1)
                elif v[-1] <= -150 and v[1] == '2':
                    t.ReqOrderInsert('cu1311', 3, 1, price, 1)
                elif v[-1] <= -150 and v[1] == '3':
                    t.ReqOrderInsert('cu1311', 3, 0, price, 1)
        time.sleep(0.5)
    #print t.investorPosition




if __name__ == '__main__':
    main()
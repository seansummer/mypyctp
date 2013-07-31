# -*- coding: utf-8 -*-

import time, ConfigParser, logging, MApi, linecache, TApi, cxh
from ctp import ApiStruct, MdApi, TraderApi   

def main():
    t = TApi.tconnect()
    time.sleep(3)
    config = ConfigParser.ConfigParser()
    config.readfp(open('./config/config.cfg'))
    profitamount = config.get('ACCOUNT', 'ProfitAmount')
    lossamount = config.get('ACCOUNT', 'LossAmount')
    cxhinstrument = config.get('ACCOUNT','CXHInstrument')
    print cxhinstrument, profitamount, lossamount
    while True:
        t.ReqQryInvestorPosition()
        time.sleep(2)
        md = cxh.getlastmd()
        price = md.split('|')[1]
        buyprice = md.split('|')[-4]
        sellprice = md.split('|')[-2]
        if t.investorPosition <> []:
            #print time.strftime("%H:%M:%S", time.localtime(time.time())),t.investorPosition
            for v in t.investorPosition:
            #v[1] 2多头 3空头
                if v[2] > 0:
                    positionProfit = v[-1]/v[2]
                    #print positionProfit
                    if positionProfit >= profitamount:
                        lossamount = profitamount
                        profitamount = profitamount * 2
                        #print lossamount,profitamount
                    if positionProfit >= profitamount and v[1] == '2':
                        t.ReqOrderInsert(cxhinstrument, 3, 1, sellprice, v[2])
                    elif positionProfit >= profitamount and v[1] == '3':
                        t.ReqOrderInsert(cxhinstrument, 3, 0, buyprice, v[2])
                    elif positionProfit < lossamount and v[1] == '2':
                        t.ReqOrderInsert(cxhinstrument, 3, 1, price, v[2])
                    elif positionProfit < lossamount and v[1] == '3':
                        t.ReqOrderInsert(cxhinstrument, 3, 0, price, v[2])
                if v[2] == 0:
                    profitamount = config.get('ACCOUNT', 'ProfitAmount')
                    lossamount = config.get('ACCOUNT', 'LossAmount')
        time.sleep(0.5)
    #print t.investorPosition




if __name__ == '__main__':
    main()
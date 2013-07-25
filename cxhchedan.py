# -*- coding: utf-8 -*-

import time, ConfigParser, logging, MApi, linecache, TApi
from ctp import ApiStruct, MdApi, TraderApi   

def timedelay(t1, t2):
    return abs(time.mktime(time.strptime(t1,'%H:%M:%S'))) - abs(time.mktime(time.strptime(t2, '%H:%M:%S')))

def main():
    t = TApi.tconnect()
    time.sleep(3)
    #t.ReqQryExchange()
    while True:
        t.qryOrder = []
        t.ReqQryOrder()
        time.sleep(10)
        if t.qryOrder <> []:
            #print t.qryOrder
            nowtime = time.strftime("%H:%M:%S", time.localtime(time.time()))
            for v in t.qryOrder:
                if timedelay(v[-1], nowtime) > 5:
                    t.ReqOrderAction(v[4], v[3])
        time.sleep(0.5)
                


if __name__ == '__main__':
    main()
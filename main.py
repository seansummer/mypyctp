# -*- coding: utf-8 -*-
import TApi, MApi, time

def main():
    menu = ['0 结算单确认','1 查询合约行情', '2 查询资金', '3 报单查询','4 成交查询', '5 持仓查询', '6 合约下单']
    t = TApi.connect()
    menucomm = {'0':t.ReqSettlementInfoConfirm,
                '1':t.ReqQryDepthMarketData,
                '2':t.ReqQryTradingAccount,
                '3':t.ReqQryOrder,
                '4':t.ReqQryTrade,
                '5':t.ReqQryInvestorPositionDetail,
                '6':t.ReqOrderInsert,
                }
    time.sleep(1)
    while True:
        for view in menu:
            print view
        comm = raw_input('请输入命令序号:')
        if str(comm) in menucomm.keys():
            menucomm[str(comm)]()
        else:
            print '错误的命令序号!'
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '终止程序'

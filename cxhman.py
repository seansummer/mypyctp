# -*- coding: utf-8 -*-
import TApi, MApi, time, ConfigParser, subprocess

    
def main():
    p1 = subprocess.Popen(["python2.7","MApi.py"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["python2.7","cxh.py"], stdout=subprocess.PIPE)
    p3 = subprocess.Popen(["python2.7","cxhpingcang.py"], stdout=subprocess.PIPE)
    p4 = subprocess.Popen(["python2.7","cxhchedan.py"], stdout=subprocess.PIPE)
    print p1.pid,p2.pid,p3.pid,p4.pid
    while 1:
        pass
    

if __name__ == '__main__':
    main()
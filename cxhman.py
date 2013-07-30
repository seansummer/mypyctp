# -*- coding: utf-8 -*-
import TApi, MApi, time, ConfigParser, subprocess

    
def main():
    p1 = subprocess.Popen(["python2.7","MApi.py"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["python2.7","cxh.py"], stdout=subprocess.PIPE)
    print p1.pid
    print p2.pid
    time.sleep(20)
    p2.kill()
    while 1:
        pass
    

if __name__ == '__main__':
    main()
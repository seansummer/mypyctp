# -*- coding: cp936 -*-
class tt:
    def one(self):
        print 'one'

    def two(self):
        print 'two'


def main():
    menu = ['1 һ������','2 ��������']
    t = tt()
    menuComm = {'1':t.one,
            '2':t.two}
    while True:
        for view in menu:
            print view
        comm = raw_input('please input num:')
        if str(comm) in menuComm.keys():
            menuComm[str(comm)]()
        else:
            print 'wrong num!'

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'stop app!'
        

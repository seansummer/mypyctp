'''
Created on Jun 4, 2013

@author: root
'''
import ConfigParser

def configread():
    config = ConfigParser.ConfigParser()
    config.readfp(open( './config/config.cfg'))
    print config.get('ACCOUNT', 'UserID')
    print config.get('ACCOUNT', 'BrokerID')

if __name__ == '__main__':
    configread()
    pass
#!/usr/bin/env python
import os

def checkCity(city):
    s = input(city)
    while len(s) != 3 or not s.isalpha():
        print('must be 3 letters')
        s = input(city)
    else:
        return s

def checkOctet(octet):
    s = input(octet)
    while len(s) > 3 or not s.isdigit():
            print('must be 3 digits')
            s = input(octet)
    else:
        return s

def checkTun(tun):
    s = input(tun)
    while not s.isdigit() or int(s) not in range(256):
        print('must be digits in range 256')
        s = input(tun)
    else:
        return s

def checkNet(net):
    s = input(net)
    while str(s).count('.') != 3:
        print('wrong format')
        s = input(net)
    else:
        l = s.split('.')
        counter = 0
        for i in l:
            while not i.isdigit() or int(i) not in range(256):
                print('{} - not in range or not digit'.format(i))
                counter = 0
                s = input(net)
            else:
                counter +=1          
        if counter == 4:
            return s

def checkMask(mask):
    s = input(mask)
    while str(s).count('.') != 3:
        print('wrong format')
    else:
        l = s.split('.')
        counter = 0
        n = []
        for a in range(9):
            n.append(256 - 2 ** a)
        for i in l:
            if not i.isdigit() or int(i) not in range(256) or i not in n:
                print('{} - not in range or not digit'.format(i))
                counter = 0
                s = input(mask)
            else:
                counter +=1
        if counter == 4:
            return s

def checkConn(conn):
    s = input(conn)
    connVars = {'dhcp': 'dhcp', 'manual': 'manual', 'pppoe': 'pppoe'}
    if s not in connVars.keys():
        print('must be dhcp/manual/pppoe')
        s = input(conn)
    else:
        return s

keyConfig = input('key config-key password-encrypt ')
enablePass = input('enable password ')
stlocalPass = input('stlocal password ')
eigrpKey = input('EIGRP_KEY_DMVPN ')
dmvpnKey = input('DMVPNKEY ')
city = checkCity('Branch city name: ekb, spb etc.. ')
secondOctet = checkOctet('Branch city 2nd octet ')
dnsPrimary = checkNet('Primary DNS IP ')
dnsSecondary = checkNet('Secondary DNS IP ')
tunnelIP = checkTun('Tunnel IP last octet (SPOKE# + 10) ')
nbmaPrimary = checkNet('Primary NBMA ')
nbmaSecondary = checkNet('Secondary NBMA ')
radiusKey = input('Radius key ')

params = {
    'XXXX': keyConfig,
    'YYYY': enablePass,
    'ZZZZ': stlocalPass,
    'WWWW': eigrpKey,
    'VVVV': dmvpnKey,
    'AAAA': city,
    'BBBB': secondOctet,
    'CCCC': dnsPrimary,
    'DDDD': dnsSecondary,
    'EEEE': tunnelIP,
    'FFFF': nbmaPrimary,
    'GGGG': nbmaSecondary,
    'UUUU': radiusKey
}

connType = checkConn('dhcp/manual/pppoe ')
if connType == 'manual':
    wanIP = checkNet('WAN IP ')
    wanMASK = checkMask('WAN IP subnet mask ')
    wanGW = checkNet('WAN default gateway ')
    params['HHHH'] = wanIP
    params['IIII'] = wanMASK
    params['JJJJ'] = wanGW
elif connType == 'pppoe':
    hostname = input('Enter pppoe login')
    password = input('Enter pppoe password')
    params['HHHH'] = hostname
    params['IIII'] = password
elif connType == 'dhcp':
    pass

# your path here
#dirPath = '/home/user/'
fileName = 'rt-aaa-bs-##_{}.txt'.format(connType)

with open(os.path.join(dirPath, fileName)) as draft, \
     open(os.path.join(dirPath, 'rt-' + city + '-cs-01.txt'), 'w') as newFile:
    lines = draft.readlines()
    for line in lines:
        for key in params.keys():
            if key in line:
                newLine = line.replace(key, params[key])
                line = newLine
        newFile.write(line)

draft.close()
newFile.close()

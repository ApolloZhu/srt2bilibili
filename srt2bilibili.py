#!/usr/bin/env python
#coding:utf-8
# Author:  Beining --<ACICFG>
# Purpose: A batch poster of srt file to danmaku on Bilibili.
# Created: 11/23/2014
# srt2Bilibili is licensed under GNUv2 license
'''
srt2Bilibili 0.03
Beining@ACICFG
cnbeining[at]gmail.com
http://www.cnbeining.com
https://github.com/cnbeining/srt2bilibili
GNUv2 license
'''

VER = '0.03'

import sys
if sys.version_info < (3, 0):
    sys.stderr.write('ERROR: Python 3.0 or newer version is required.\n')
    sys.exit(1)
try:
    import requests
except:
    sys.stderr.write('ERROR: Requests is required. Please check https://github.com/cnbeining/srt2bilibili#usage .\n')
    sys.exit(1)
try:
    import pysrt
except:
    sys.stderr.write('ERROR: Pysrt is required. Please check https://github.com/cnbeining/srt2bilibili#usage .\n')
    sys.exit(1)

import logging
import time as time_old
import getopt
from random import randint

#----------------------------------------------------------------------
def find_cid_api(vid, p):
    """find cid and print video detail
    str,int->int"""
    try:
        info = requests.get('http://www.bilibili.com/widget/getPageList?aid='+str(vid)).json()
        logging.debug(info)
        p = min((p < 1 and 1 or p), len(info))
        return int(info[p - 1]["cid"])
    except:
        logging.warning("Failed to get cid")
        return 0

#----------------------------------------------------------------------
def convert_cookie(cookie_raw):
    """str->dict
    'DedeUserID=358422; DedeUserID__ckMd5=; SESSDATA=72e0ee97%%2C6b47a180'
    cookie = {'DedeUserID': 358422, 'DedeUserID__ckMd5': '', 'SESSDATA': '72e0ee97%%2C6b47a180'}"""
    cookie = {}
    logging.debug('Raw Cookie: ' + cookie_raw)
    try:
        for i in [i.strip() for i in cookie_raw.split(';')]:
            cookie[i.split('=')[0]] = i.split('=')[1]
    except IndexError:
        #if someone put a ; at the EOF
        pass
    return cookie

#----------------------------------------------------------------------
def getdate():
    """None->str
    2014-11-23 10:39:46"""
    return time_old.strftime("%Y-%m-%d %X", time_old.localtime())

#----------------------------------------------------------------------
def post_one(message, rnd, cid, cookie, fontsize = 25, mode = 4, color = 16777215, playTime = 0, pool = 0, fake_ip = False):
    """
    PARS NOT THE PERFECT SAME AS A PAYLOAD!"""
    headers = {'Origin': 'http://static.hdslb.com', 'X-Requested-With': 'ShockwaveFlash/15.0.0.223', 'Referer': 'http://static.hdslb.com/play.swf', 'User-Agent': BILIGRAB_UA, 'Host': 'interface.bilibili.com', 'Content-Type': 'application/x-www-form-urlencoded'}
    if fake_ip:
        FAKE_IP = ".".join(str(randint(1, 255)) for i in range(4))
        headers.update({'X-Forwarded-For' : FAKE_IP, 'Client-IP' : FAKE_IP})
    #print(headers)
    url = 'http://interface.bilibili.com/dmpost'
    try:
        payload = {'fontsize': fontsize, 'message': message, 'mode': mode, 'pool': pool, 'color': color, 'date': getdate(), 'rnd': rnd, 'playTime': playTime, 'cid': cid}
        r = requests.post(url, data = payload, headers = headers, cookies=cookie)
        #print(r.text)
        if int(r.text) <= 0:
            logging.warning('Line failed:')
            logging.warning('Message:' + str(message))
            logging.warning('ERROR Code: ' + str(r.text))
        else:
            print(message)
        #logging.info(message)
    except Exception as e:
        print('ERROR: Line failed: %s' % e)
        print('Payload:' + str(payload))

#----------------------------------------------------------------------
def timestamp2sec(timestamp):
    """SubRipTime->float
    SubRipTime(0, 0, 0, 0)"""
    return (int(timestamp.seconds) + 60 * int(timestamp.minutes) + 3600 * int(timestamp.hours) + float(int(timestamp.hours) / 1000))

#----------------------------------------------------------------------
def read_cookie(cookiepath):
    """str->list
    Original target: set the cookie
    Target now: Set the global header
    From: Biligrab, https://github.com/cnbeining/Biligrab
    MIT License"""
    try:
        with open(cookiepath, 'r') as cookies_file:
            cookies = cookies_file.readlines()
            # print(cookies)
            return cookies
    except:
        logging.warning('Cannot read cookie!')
        return ['']

#----------------------------------------------------------------------
def main(srt, fontsize, mode, color, cookie, aid, p = 1, cool = 3.5, pool = 0, fake_ip = False):
    """str,int,int,int,str,int,int,int,int->None"""
    rnd = randint(0, 1000000000)
    cid = find_cid_api(aid, p)
    subs = pysrt.open(srt)
    for sub in subs:
        #lasttime = timestamp2sec(sub.stop) - timestamp2sec(sub.start)
        # For future use
        playtime = timestamp2sec(sub.start)
        message = sub.text
        if '\n' in message:
            for line in message.split('\n'):
                post_one(line, rnd, cid, cookie, fontsize, mode, color, playtime, pool,fake_ip = fake_ip)
                time_old.sleep(cool)
        else:
            post_one(message, rnd, cid, cookie, fontsize, mode, color, playtime, pool,fake_ip = fake_ip)
            time_old.sleep(cool)
    print('INFO: DONE!')


#----------------------------------------------------------------------
def usage():
    """"""
    print('''
    srt2Bilibili
    
    https://github.com/cnbeining/srt2bilibili
    http://www.cnbeining.com/
    
    Beining@ACICFG
    
    WARNING: THIS PROGRAMME CAN BE DANGEROUS IF MISUSED,
    AND CAN LEAD TO UNWANTED CONSEQUNCES,
    INCLUDING (BUT NOT LIMITED TO) TEMPORARY OR PERMANENT BAN OF ACCOUNT AND/OR
    IP ADDRESS, DANMAKU POOL OVERSIZE, RUIN OF NORMAL DANMAKU.
    
    ONLY USE WHEN YOU KNOW WHAT YOU ARE DOING.
    
    This program is provided **as is**, with absolutely no warranty.
    
    
    Usage:
    
    python3 srt2bilibili.py (-h) (-a 12345678) [-p 1] [-c ./bilicookies] (-s 1.srt) [-f 25] [-m 4] [-o 16777215] [-w 3.5] [-l 0] (-i)
    
    -h: Default: None
        Print this usage file.
        
    -a: Default: None
        The av number.
        
    -p: Default: 1
        The part number.
        
    -c Default: ./bilicookies
        The path of cookies.
        Should looks like:
        
        DedeUserID=123456;DedeUserID__ckMd5=****************;SESSDATA=*******************
            
    -s Default: None
        The srt file you want to post.
        srt2bilibili will post multi danmakues for multi-line subtitle,
        since there's a ban on the use of \n.
        
    -f Default: 25
        The size of danmaku.
        
    -m Default: 4
        The mode of danmaku.
        1: Normal
        4: Lower Bound  *Suggested
        5: Upper Bound
        6: Reverse
        7: Special
        9: Advanced
        
    -o Default: 16777215
        The color of danmaku, in integer.
        Default is white.
        
    -w Default: 3.5
       The cool time (time to wait between posting danmakues)
       Do not set it too small, which would lead to ban or failure.
       
    -l Default: 0
        The Danmaku Pool to use.
        0: Normal
        1: Subtitle
        2: Special
        If you own the video, please set it to 1 to prevent potential lost of danmaku.
        
    -i Default: False
        Use a fake IP address for every comment.
    
    More info available at http://docs.bilibili.cn/wiki/API.comment.
    ''')

#----------------------------------------------------------------------
if __name__=='__main__':
    argv_list = []
    argv_list = sys.argv[1:]
    aid, part, cookiepath, srt, fontsize, mode, color, cooltime, playtime, pool, fake_ip = 0, 1, './bilicookies', '', 25, 4, 16777215, 3.5, 0, 0, False
    try:
        opts, args = getopt.getopt(argv_list, "ha:p:c:s:f:m:o:w:l:i",
                                   ['help', "av", 'part', 'cookie', 'srt', 'fontsize', 'mode', 'color', 'cooltime', 'pool', 'fake-ip'])
    except getopt.GetoptError:
        usage()
        exit()
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            exit()
        if o in ('-a', '--av'):
            aid = a
            try:
                argv_list.remove('-a')
            except:
                break
        if o in ('-p', '--part'):
            try:
                part = int(a)
                argv_list.remove('-p')
            except:
                part = 1
        if o in ('-c', '--cookie'):
            cookiepath = a
            try:
                argv_list.remove('-c')
            except:
                print('INFO: No cookie path set, use default: ./bilicookies')
                cookiepath = './bilicookies'
        if o in ('-s', '--srt'):
            srt = a
            try:
                argv_list.remove('-s')
            except:
                break
        if o in ('-f', '--fontsize'):
            try:
                fontsize = int(a)
                argv_list.remove('-f')
            except:
                fontsize = 25
        if o in ('-m', '--mode'):
            try:
                mode = int(a)
                argv_list.remove('-m')
            except:
                mode = 4
        if o in ('-o', '--color'):
            try:
                color = int(a)
                argv_list.remove('-o')
            except:
                color = 16777215
        if o in ('-w', '--cooltime'):
            try:
                cooltime = float(a)
                argv_list.remove('-w')
            except:
                cooltime = 3.5
        if o in ('-l', '--pool'):
            try:
                pool = int(a)
                argv_list.remove('-l')
            except:
                pool = 0
        if o in ('-i', '--fake-ip'):
            fake_ip = True
    if aid == 0:
        logging.fatal('No aid!')
        exit()
    if srt == '':
        logging.fatal('No srt!')
        exit()
    if len(cookiepath) == 0:
        cookiepath = './bilicookies'
    cookies = convert_cookie(read_cookie(cookiepath)[0])
    logging.debug('Cookies: ' + str(cookiepath))
    logging.debug(cookies)
    BILIGRAB_UA = 'srt2Bilibili / ' + str(VER) + ' (cnbeining@gmail.com)'
    main(srt, fontsize, mode, color, cookies, aid, part, cooltime, pool, fake_ip = fake_ip)

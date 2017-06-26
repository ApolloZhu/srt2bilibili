srt2bilibili
============

A batch poster of srt file to danmaku on Bilibili.

Fully automatic once started.

Usage
------

If you have a Bilibili account, set the cookie with https://github.com/dantmnf/biliupload/blob/master/getcookie.py  will help you to download some of the restricted videos. Also you can do that by hand.

The file should looks like:

    DedeUserID=123456;DedeUserID__ckMd5=****************;SESSDATA=*******************

Command line mode:

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


Requirement
-------

- Python 3.x
- pysrt (Avalable at https://pypi.python.org/pypi/pysrt), or just `sudo pip3 install pysrt`(may vary on machines)
- requests (Avalable at http://docs.python-requests.org/en/latest/user/install/#install), or just `sudo pip3 install requests` / `easy_install requests`(may vary on machines)

Author
-----

Beining, http://www.cnbeining.com/

License
-----

GPLv2 license.

This program is provided **as is**, with absolutely no warranty.


Contributing
------------

Any contribution is welcome. 

*You can still send me the info privately via my email. PGP public key avalable at http://www.cnbeining.com/about/*

Any donation is welcome as well. Please get in touch with me: cnbeining[at]gmail.com .

Misc
-----

    WARNING: THIS PROGRAMME CAN BE DANGEROUS IF MISUSED,
    AND CAN LEAD TO UNWANTED CONSEQUNCES,
    INCLUDING (BUT NOT LIMITED TO) TEMPORARY OR PERMANENT BAN OF ACCOUNT AND/OR
    IP ADDRESS, DANMAKU POOL OVERSIZE, RUIN OF NORMAL DANMAKU.
    
    ONLY USE IF YOU KNOW WHAT YOU ARE DOING.

History
----
0.03: Changed default parameter values for consistency and more promising results. Introduced a new implementation of CID fetching.

0.02.2 alpha: Add IP faking.

0.02.1: Add error handling if requirements not met.

0.02: Error handling with cookies; Clean headers; Change default values for quicker posting and better subtitle.

0.01: The very start

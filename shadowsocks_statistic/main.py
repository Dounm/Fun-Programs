#!/usr/bin/env python

import sys
import os
import subprocess
import datetime
import json

sys.path.append(sys.path[0]+'/..')
import util.email_sender


def get_cur_day():
    today = datetime.datetime.today()
    year = str(today.year)
    month = ''
    day = ''
    if today.month < 10:
        month = '0'
    month = month + str(today.month)
    if today.day < 10:
        day = '0'
    day = day + str(today.day)
    return year + '-' + month + '-' + day

def grep_logfile(log_file, cur_day):
    cmd = 'grep ' + cur_day + ' ' + log_file + ' | grep from'
    #try:
    grep_res = subprocess.check_output(cmd, shell=True)
    """
    finally:
        print 'no connections at', cur_day
        exit(1)
    """
    return grep_res.split('\n')

def extract_connected_ips(lines):
    ip_dict = {}
    domain_set = set(['com', 'edu', 'org'])
    for line in lines:
        #get the specific ip
        pos1 = line.find('from')
        pos2 = line.find(':', pos1)
        ip = line[pos1+5:pos2]
        #get the destination
        tmp = line[line.find('connecting')+10 : line.find('from')]
        tmp = tmp.split('.')
        dest = tmp[len(tmp)-2]
        if dest in domain_set:
            dest = tmp[len(tmp)-3]

        if ip in ip_dict:
            ip_dict[ip].add(dest) 
        else:
            ip_dict[ip] = set([dest])
    del ip_dict['']
    print ip_dict
    return ip_dict

def send_email(ip_dict, config_file, cur_day):
    subject = 'The connections to shadowsocks server of ' + cur_day
    msg = '\n'
    for k in ip_dict:
        msg += '[%s]' % k + ' has connected the sites below in %s:\n\t' % cur_day
        for domain in ip_dict[k]:
            msg += domain + ', '
        msg += '\n'
        msg += '\n'
    msg += '\n'

    d = dict()
    with open(config_file, 'r') as f:
        d = json.load(f)
    util.email_sender.send_email(str(d['sender']), str(d['sender_pwd']), \
        str(d['receiver']), subject, msg)

log_file = sys.argv[1]
config_file = sys.argv[2]

cur_day = get_cur_day()
lines_list = grep_logfile(log_file, cur_day)
ip_dict = extract_connected_ips(lines_list)
send_email(ip_dict, config_file, cur_day)

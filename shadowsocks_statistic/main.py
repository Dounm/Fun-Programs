#!/usr/bin/env python

import sys
sys.path.append('..')
import subprocess
import datetime
import json

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
    for line in lines:
        pos1 = line.find('from')
        pos2 = line.find(':', pos1)
        ip = line[pos1+5:pos2]
        if ip in ip_dict:
            ip_dict[ip] += 1
        else:
            ip_dict[ip] = 1
    del ip_dict['']
    return ip_dict

def send_email(ip_dict, config_file, cur_day):
    subject = 'The connections to shadowsocks server of ' + cur_day
    msg = '\n'
    for k in ip_dict:
        msg += '[%s]' % k + ' connected ' + str(ip_dict[k]) + ' times in ' + cur_day + '\n'
    msg += '\n'

    d = dict()
    with open(config_file, 'r') as f:
        d = json.load(f)
        print d
    util.email_sender.send_email(str(d['sender']), str(d['sender_pwd']), \
        str(d['receiver']), subject, msg)

log_file = sys.argv[1]
config_file = sys.argv[2]

cur_day = get_cur_day()
lines_list = grep_logfile(log_file, cur_day)
ip_dict = extract_connected_ips(lines_list)
print ip_dict
send_email(ip_dict, config_file, cur_day)

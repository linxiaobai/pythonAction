#!/usr/bin/python

import os
import sys
import codecs
import time
import datetime

ack_path = "/opt/shell/ack/"
base_path = "/opt/shell/vids/"
suffix = ".txt"
scp_command = "scp /data/%s.mp4 root@10.xx.xx.21:/data/video/"
check_command = "ssh root@10.xx.xx.21 \" ls /data/video/%s.mp4 | wc -l \""

def get_file_lines(file_path):
	f = codecs.open(file_path, 'r','utf-8')
	line_list =  f.readlines()
	f.close()
	return line_list

def get_time():
	return ((datetime.datetime.now()-datetime.timedelta(minutes=2)).strftime("%Y%m%d%H%M"))

def get_vid(vid_str):
	return vid_str.split("#")[0]

def record_failed_vid(failed_vid):
	today = datetime.date.today()
    record_file=base_path + today.strftime('%Y-%m-%d') + suffix
    file_is_exist = os.path.exists(record_file)
    if(not file_is_exist):
            os.system("touch %s" % record_file)
    f = codecs.open(record_file, 'a', 'utf-8')
    f.write(failed_vid + "\n")



def run_scp(vid):
	count = 0
	while True:
		run_scp_cmd = scp_command % vid
		print "scp command:" + run_scp_cmd
		ret = os.system(run_scp_cmd)
		print "scp ret:" + str(ret)
		run_ck_cmd = check_command % vid
		print "check command:" + run_ck_cmd
		ret = os.popen(run_ck_cmd).read()
		print "check ret:" + str(ret)
		if(int(ret) > 0):
			print "scp success,check ret:" + str(ret)
			break
		elif(count > 5):
			print "too many failed,vid:" + vid
			record_failed_vid(vid)
			break
		else:
			count = count + 1
			print "scp failed, than retry " + str(count)

def touch_ack_file(file):
	file_path = ack_path + file
	os.system("touch %s" % file_path)

if __name__=='__main__':
	time = get_time()
	file_name = time + suffix
	file = base_path + file_name
	file_is_exist = os.path.exists(file)
	if(not file_is_exist):
		print "file not exist:" + file
	else:
		print "deal with file:" + file
		vid_list=get_file_lines(file)
		for vid_str in vid_list:
			vid=get_vid(vid_str)
			run_scp(vid)
		touch_ack_file(file_name)


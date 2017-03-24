#!/usr/bin/python
##by linxiaobai@live.com
##a test shell for compare guetzli
# -*- coding: utf-8 -*-

import os
from time import time

quality = 85
pics_dir_path = "/opt/pictttt/"
pics_out_path = "/opt/picttttout/"
prefix = "guetzli-"
guetzli_shell = "guetzli --quality %d %s %s"
gm_shell = "gm -convert -quality %d %s %s"

class RunShellError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		repr(self.value)


def run_shell(command):
	print "run shell `", command, "`"
	ret = os.system(command)
	if (ret != 0):
		raise RunShellError("run `" + command + "` failed, ret:" +  str(ret))

def get_all_pic(path):
	list = os.listdir(path)
	print "all pic count is:",len(list)
	return list

def get_out_name(pic):
	return prefix + pic

##unit is KB
def get_file_size(pic_path):
	return os.path.getsize(pic_path) / 1024

def get_percent(out_put_size, original_size):
	percent = round(out_put_size * 100 / original_size, 2)
	return percent

def compress(pic):
	print "start compress pic:", pic
	start_time = time()
	out_name = get_out_name(pic)
	original_pic_size = get_file_size(pics_dir_path + pic)
	shell = guetzli_shell  % (quality, pics_dir_path + pic, pics_out_path + out_name)
	run_shell(shell)
	end_time = time()
	generate_pic_size = get_file_size(pics_out_path + out_name)
	percent = get_percent(generate_pic_size, original_pic_size)
	print "compress pic %s end, original size %d KB, generate size %d KB, compress percent %d %% , cost time: %d s." % (pic, original_pic_size, generate_pic_size, percent, (end_time - start_time)) 


if __name__=='__main__':
	start_time = time()
	print "###start guetzli test###"
	pic_list = get_all_pic(pics_dir_path)
	for pic in pic_list:
		compress(pic)
	end_time = time()
	print "###guetzli test end###"
	print "total cost time: %d s" % (end_time - start_time)

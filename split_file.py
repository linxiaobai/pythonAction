#!/usr/bin/python
##by linxiaobai@live.com
##split file when file more than 10M, divide into part size 7M files
import os
import sys
import math
import codecs

part_size = 1024 * 1024 * 7
prefix = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n<urlset>\n"
suffix = "</urlset>"

def get_file_size(file_path):
	return os.path.getsize(file_path)

def get_ceil_number(total_size, part_size):
	return int(math.ceil(float(total_size) / part_size))

def get_file_lines(file_path):
	f = codecs.open(file_path, 'r','utf-8')
	line_list =  f.readlines()
	f.close()
	return line_list

def print_list(lines_list):
	for line in lines_list:
		print line.strip()

def strcat(str1, str2):
	combine_str = str1 + str(str2) + ".xml"
	print "combine str: ", combine_str
	return combine_str


def split_file(lines_list, part):
	all_lines = len(lines_list)
	part_lines = get_ceil_number(all_lines, part)
	print "all line:%d, divide part lines:%d" % (all_lines, part_lines)
	idx = 1
	file_prefix = file_path.split(".xml")[0]
	print "new file prefix:", file_prefix
	f = codecs.open(strcat(file_prefix,idx), 'w', 'utf-8')
	for i in range(0,all_lines):
		line = lines_list[i]
		f.write(line)
		if i > idx * part_lines and line.strip() == "</url>":
			f.write(suffix)
			f.close()
			idx = idx + 1
			f = codecs.open(strcat(file_prefix, idx), 'w', 'utf-8')
			f.write(prefix)
	f.close
	return idx


if __name__=='__main__':
	#accept param, for example: python split_file.py xx.xml, the sys.argv[1] -> xx.xml
	file_path = sys.argv[1]
	print "split part size:",part_size
	file_size = get_file_size(file_path) 
	print "file size:",file_size
	part = get_ceil_number(file_size, part_size)
	print "divide part:",part
	if part == 1:
		print "needn't to split file"
		sys.exit(0)
	else:
		print "start split file"
		lines_list = get_file_lines(file_path)
		#print_list(lines_list)
		idx = split_file(lines_list, part)
		print "split file end,idx: ", idx
		sys.exit(idx)
	


	


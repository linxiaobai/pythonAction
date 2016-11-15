#!/usr/bin/python
##add by linxiaobai@live.com
##combine sohu edu data to sogou,baidu,360 page common data
import os
import sys
import codecs



channels = ("baidu", "bing", "sogou")
common_prefix = "page_"
common_suffix = ".xml"
common_path = "/opt/sitemap/"
edu_path = "/opt/sitemap/sohuedu/page.xml"
filter_str = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>", "<urlset>")

def check_is_combined(data_list):
	for x in xrange(-20,-1):
		if (data_list[x].strip().find("edu.tv.sohu.com") >= 0):
			return True
	return False

def combine_data(xml_name, channel_data, edu_data):
	if (check_is_combined(channel_data)):
		print xml_name + "has already combined edu data"
		return
	f = codecs.open(xml_name, 'w', 'utf-8')
	channel_data_size = len(channel_data)
	for i in range(0, channel_data_size):
		line = channel_data[i]
		if i == channel_data_size - 1: #start append sohu edu data
			for edu_line in edu_data:
				if edu_line.strip() not in filter_str:
					f.write(edu_line)
		else:
			f.write(line)
	f.close()
	print "combine " + xml_name + " success!"


def read_xml_to_list(path):
	f = codecs.open(path, 'r','utf-8')
	data_list = f.readlines()
	f.close()
	return data_list

if __name__=='__main__':
	sohu_edu_data = read_xml_to_list(edu_path)
	for channel in channels:
		path = common_path + common_prefix + channel + common_suffix
		print path
		data_list = read_xml_to_list(path)
		combine_data(path, data_list, sohu_edu_data)

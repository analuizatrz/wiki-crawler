# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError
from datetime import datetime
import requests
import csv
import sys
import json
import time

class Logger(object):
	def __init__(self, message=None, filepath=None):
		self.message = message
		self.filepath = filepath
		self.articles_array = []

	def smessage(self, message):
		self.message = message
		return self

	def set_articles(self, articles_array):
		self.articles_array = articles_array
		return self

	def error_parsing_articles(self):
		articles_string = ",".join(self.articles_array)
		print(f"Error parsing articles: {articles_string}")

	def requesting_articles(self):
		print("requesting articles")

	def log(self, message=None):
		if message is not None:
			self.message = message
		if self.message is not None:
			if self.filepath is None:
				print(self.message)
			else:
				with open(self.filepath) as txt_file:
					txt_file.write(self.message)

	def read_json(self):
		with open(self.filepath, 'r') as fp:
			return json.load(fp)

	def write_json(self, content):
		with open(self.filepath, 'w') as fp:
			json.dump(content, fp)

class HTMLParser(object):
	def __init__(self, logger=None):
		if logger:
			self.logger = logger
		else:
			self.logger = Logger()

	def parse(self, text):
		try: 
			return HTMLNode(parseString(text))
		except ExpatError:
			self.logger.log()
		return None

class HTMLNode(object):
	def __init__(self, dom):
		self.dom = dom

	def get_data(self, tag):
		tag = self.dom.getElementsByTagName(tag)
		if(len(tag) > 0 and len(tag[0].childNodes) > 0):
			return tag[0].childNodes[0].data.strip()
		return None

	def get_elements(self, tag_name):
		return [HTMLNode(p) for p in self.dom.getElementsByTagName(tag_name)]

class BaseCrawler(object):
	def __init__(self):
		self.html_parser = HTMLParser()

	def request(self, url, body=None, logger=None, parser=None):
		r = requests.post(url, data=body)
		if logger:
			logger.requesting_articles()
		if parser:
			parser.parse(r.text)
		return HTMLParser().parse(r.text)
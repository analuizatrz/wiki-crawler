# -*- coding: utf-8 -*-

from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError
import csv
import requests
import sys


OFFSET = "2017-10-01T00:00:00Z"
DIRECTION = "DESC"
LIMIT = "1"

def request_wiki(articles_array):
	data = {"pages":"\n".join(articles_array),
			"offset":OFFSET,
			"dir":DIRECTION,
			"limit":LIMIT, # 
			"action":"submit",
			"title":"Special:Export"}

	url_to_request = "https://en.wikipedia.org/w/index.php"
	r = requests.post(url_to_request, data=data)
	print("Requisitando: "+str(len(articles_array))+" páginas")
	#print(r.text)
	try:
		return parseString(r.text)
	except ExpatError:
		print("deu erro")
		return None

def get_tag_data(dom, tag):
	tag = dom.getElementsByTagName(tag)
	if(len(tag) > 0 and len(tag[0].childNodes) > 0):
		return tag[0].childNodes[0].data.strip()
	return None

def get_pages(articles):
	dom = request_wiki(articles)

	pages = dom.getElementsByTagName("page")

	for page in pages:
		page_id = get_tag_data(page, "id")
		title = get_tag_data(page, "title")
		revision_element = page.getElementsByTagName("revision")[0]
		wiki_text = get_tag_data(revision_element, "text")
		print(f"id: {page_id} title: {title} wiki_text: (just the begging) {wiki_text[0:10]}")

def read_first_column(csv_filepath):
	with open(csv_filepath) as csvfile:
		return [row[0] for row in list(csv.reader(csvfile))]

input_file = sys.argv[1]

count = 3
articles = read_first_column(input_file)[:count]
first_articles = articles[:count]

get_pages(first_articles)
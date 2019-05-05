# -*- coding: utf-8 -*-

from base_crawler import HTMLNode, HTMLParser
from sys import argv
import csv
import requests

OFFSET = "2017-10-01T00:00:00Z"
DIRECTION = "DESC"
LIMIT = "1"

def request_wiki(articles_array):
	data = {"pages":"\n".join(articles_array),
			"offset":OFFSET,
			"dir":DIRECTION,
			"limit":LIMIT,
			"action":"submit",
			"title":"Special:Export"}

	url_to_request = "https://en.wikipedia.org/w/index.php"
	r = requests.post(url_to_request, data=data)
	print("Requisitando: "+str(len(articles_array))+" páginas")
	return HTMLParser().parse(r.text)

def get_pages(articles):
	dom = request_wiki(articles)

	pages = dom.get_elements("page")

	for page in pages:
		page_id = page.get_data("id")
		title = page.get_data("title")
		revision_element = page.get_elements("revision")[0]
		wiki_text = revision_element.get_data("text")
		print(f"id: {page_id} title: {title} wiki_text: (just the begging) {wiki_text[0:10]}")

def read_first_column(csv_filepath):
	with open(csv_filepath) as csvfile:
		return [row[0] for row in list(csv.reader(csvfile))]

input_file = argv[1]

count = 3
articles = read_first_column(input_file)[:count]
first_articles = articles[:count]

get_pages(first_articles)
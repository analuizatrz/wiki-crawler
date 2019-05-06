# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
from base_crawler import BaseCrawler, Logger
from wiki_page import WikiPageWithClass
from wiki_utils import is_redirection, redirect
from wiki_parser import parse_talk_wikipages_with_class, WikiParser, WikiParserPageWithClass
from utils import Clock, read_first_column
import requests
import csv

import sys
import json
import time

class WikiPagesCrawler(BaseCrawler):
	def __init__(self, name, offset, direction, limit, articles_per_request):
		super().__init__()
		self.offset = "2017-10-01T00:00:00Z"
		self.arq_crawl_status = name+"_crawl_status.json"
		self.output = name+"_classes.csv"
		self.error = name+"_page_errors.csv"
		self.direction = direction
		self.limit = limit
		self.articles_per_request = articles_per_request

		self.pages_status_logger = Logger("", self.arq_crawl_status)
		self.error_logger = Logger("", self.error)
		self.output_logger = Logger("", self.output)
		self.terminal_logger = Logger("")

	def request_wiki(self, articles_array, recursion_depth=0):
		url = "https://en.wikipedia.org/w/index.php"

		body = {
			"pages":"\n".join(articles_array),
			"offset":self.offset,
			"dir":"desc",
			"limit":1,
			"action":"submit",
			"title":"Special:Export"
		}
		return super().request(url, body, self.terminal_logger)

	def request_in_bulks(self, articles_array, wiki_parser):
		status = {}
		try:
			new_status = self.pages_status_logger.read_json()
			status = new_status
		except IOError:
			status = {"collected_pages":[]}

		already_collected_pages = set(status["collected_pages"])
		remaning_to_collect = [article for article in articles_array if article not in already_collected_pages]

		objTime = Clock()
		articles_errors = []
		arr_collected_now = []

		while(len(remaning_to_collect) > 0):
			if(len(arr_collected_now) > 0):
				remaning_to_collect = list(set(remaning_to_collect) - set(arr_collected_now))
				objTime.print_delta("===> Collected articles: "+str(len(arr_collected_now))+") remaining: "+str(len(remaning_to_collect)+self.articles_per_request-len(arr_collected_now)))

			next_articles = remaning_to_collect[:self.articles_per_request]
			remaning_to_collect = remaning_to_collect[self.articles_per_request:]

			arr_collected_now = []

			HTMLNode = self.request_wiki(next_articles)
			wiki_pages = wiki_parser.parse(HTMLNode)

			# logger de error
			with open(self.output, 'a') as output_pointer, open(self.error, 'a') as error_pointer:
				csv_writer = csv.writer(output_pointer, delimiter=';',quotechar='"',quoting=csv.QUOTE_NONNUMERIC)

				print("Pages:"+str(len(wiki_pages)))

				for page in wiki_pages:
					wiki_parser.collect(page, csv_writer, status, arr_collected_now)

				self.pages_status_logger.write_json(status)

				# refactor log
				#caso nao tenha coletado nenhum agora, adicione eles como artigos com erro
				if(len(arr_collected_now) == 0):
					[error_pointer.write(title+";") for title in next_articles]
					error_pointer.write("\n")
					articles_errors = next_articles
					print("ERROR: Could not collect anything from this list:"+str(next_articles))
					time.sleep(30)
			time.sleep(1)

def test_crawler(input_file):
	input_file_name = input_file.split("/")[-1].split(".")[0]
	articles = read_first_column(input_file)[:9]

	print(articles)
	dom = WikiPagesCrawler(input_file_name, "2017-10-01T00:00:00Z", "desc", 1, 3)\
			.request_wiki(articles)

	print(dom.get_elements("page")[0].get_data("id"))
	print(dom.get_elements("page")[1].get_data("id"))
	print(dom.get_elements("page")[2].get_data("id"))

	WikiPagesCrawler(input_file_name, "2017-10-01T00:00:00Z", "desc", 1, 3)\
		.request_in_bulks(articles, WikiParserPageWithClass())

if __name__ == "__main__":
	input_file = sys.argv[1]
	test_crawler(input_file)
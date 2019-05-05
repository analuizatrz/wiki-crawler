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

def is_redirection(wiki_text):
	if wiki_text is not None:
		return wiki_text.startswith("#REDIRECT")
	return False

def redirect(wiki_text, limit=5):
	if limit >= 0:
		open_brackets = wiki_text.find("[[")
		close_brackets = wiki_text.find("]]")
		if(open_brackets > 0 and close_brackets > 0):
			redir_title = wiki_text[open_brackets+2:close_brackets]
		return redir_title
	return ""

def parse_revision_classes(text):
	classes = []
	if text is not None:
		lines = text.replace("{{","}}").replace("\n","").split("}}")
		for line in lines:
			if "class" in line:
				atributes = line.split("|")
				wiki_project = ""
				wiki_class = "-"
				for idx, atribute in enumerate(atributes):
					atribute_values = atribute.split("=")
					if idx == 0:
						wiki_project = atribute_values[0]
					if atribute_values[0] == "class" and len(atribute_values) > 1 :
						wiki_class = atribute_values[1]	
				classes.append(WikiPageClass(wiki_project, wiki_class))	
	return classes

class WikiPage(object):
	def __init__(self, id, title, classes):
		self.id = id
		self.title = title.replace("Talk:","")
		self.classes = classes

	def get_classes(self):
		classes_names = [c.wiki_class for c in self.classes]
		return "/".join(classes_names)

class WikiPageClass(object):
	def __init__(self, wiki_project, wiki_class):
		self.wiki_project = wiki_project
		self.wiki_class = wiki_class
	def __str__(self):
		return self.wiki_project+": class "+ self.wiki_class

class CheckTime(object):
	def __init__(self):
		self.time = datetime.now()
		self.sum_time = 0
		self.cont_deltas = 0

	def finish_time(self):
			delta = datetime.now()-self.time
			self.time = datetime.now()
			return delta

	def print_delta(self, task):
		delta = self.finish_time()
		self.sum_time += delta.total_seconds()
		self.cont_deltas += 1
		print(task+" done in "+str(delta.total_seconds())+" average: "+str(self.sum_time/self.cont_deltas))

class Logger(object):
	# Classe que produz log em arquivo ou no terminal (por default no terminal)
	# Para fazer log em arquivo é necessario passar o filepath
	# Caso nenhuma mensagem seja passada, nada sera loggado
	
	# Modos de uso
	#
	# logger1 = Logger("criando arquivo", "log_de_arquivo.txt")
	# logger1.log()

	# logger2 = Logger()
	# logger2.log("problema ao fazer a requisição")

	def __init__(self, message=None, filepath=None):
		self.message = message
		self.filepath = filepath

	def smessage(self, message):
		self.message = message
		return self

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
	def request(self, url, body=None, logger=None, parser=None):
		r = requests.get(url, data=body)
		if logger:
			logger.log() 
		if parser:
			return parser.parse(r.text)
		return r

class WikiPagesCrawler(BaseCrawler):
	def __init__(self, name, offset, direction, limit, articles_per_request):
		# body of the constructor
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
		self.text_parser = HTMLParser()

	def request_wiki(self, articles_array,recursion_depth=0):
		url = "https://en.wikipedia.org/w/index.php"

		body = {
			"pages":"\n".join(articles_array),
			"offset":self.offset,
			"dir":"desc",
			"limit":1,
			"action":"submit",
			"title":"Special:Export"
		}
		
		return super().request(url, body, self.terminal_logger.smessage("Requisitando: "+str(len(articles_array))+" páginas"), self.text_parser)

	def request_in_bulks(self, articles_array,recursion_depth=0):
		status = {}
		try:
			new_status = self.pages_status_logger.read_json()
			status = new_status
		except IOError:
			status = {"collected_pages":[]}
		
		collected_articles = set(status["collected_pages"])
		articles_to_collect = [article for article in articles_array if article not in collected_articles]

		objTime = CheckTime()
		articles_errors = []
		arr_collected_now = []

		while(len(articles_to_collect) > 0):	
			if(len(arr_collected_now) > 0):
				articles_to_collect = list(set(articles_to_collect) - set(arr_collected_now))
				objTime.print_delta("===> Collected articles: "+str(len(arr_collected_now))+") remaining: "+str(len(articles_to_collect)+self.articles_per_request-len(arr_collected_now)))

			articles_to_request_now = articles_to_collect[:self.articles_per_request]
			articles_to_collect = articles_to_collect[self.articles_per_request:]

			arr_collected_now = []

			wiki_pages = self.get_pages(articles_to_request_now)

			# logger de error
			with open(self.output, 'a') as output_pointer, open(self.error, 'a') as error_pointer:
				csv_writer = csv.writer(output_pointer, delimiter=';',quotechar='"',quoting=csv.QUOTE_NONNUMERIC)

				print("Pages:"+str(len(wiki_pages)))

				for page in wiki_pages:
					csv_writer.writerow([page.id, page.title, page.get_classes()])
					status["collected_pages"].append(page.title)
					arr_collected_now.append(page.title)

				self.pages_status_logger.write_json(status)

				#caso nao tenha coletado nenhum agora, adicione eles como artigos com erro
				if(len(arr_collected_now) == 0):
					[error_pointer.write(title+";") for title in articles_to_request_now]
					error_pointer.write("\n")
					articles_errors = articles_to_request_now
					print("ERROR: Could not collect anything from this list:"+str(articles_to_request_now))
					time.sleep(30)

			time.sleep(1)

	def get_pages(self, articles_to_request_now):
		HTMLNode = self.request_wiki(articles_to_request_now)
		
		pages = HTMLNode.get_elements("page")
		wiki_pages = []

		for page in pages:
			page_id = page.get_data("id")
			title = page.get_data("title")
			revision_element = page.getElementsByTagName("revision")[0]
			wiki_text = revision_element.get_data("text")
			limit = 5
			while is_redirection(wiki_text) and limit:
				redirect_title = redirect(wiki_text)
				HTMLNode = self.request_wiki([redirect_title])
				page = revision_element = HTMLNode.get_elements("page")[0]
				revision_element = page.get_elements("revision")[0]
				title = title+"/"+page.get_data("title")
				wiki_text = revision_element.get_data("text")
				limit -= 1
			classes = parse_revision_classes(wiki_text)

			wiki_pages.append(WikiPage(page_id, title, classes))
		return wiki_pages

def crawler(input_file):
	input_file_name = input_file.split("/")[-1].split(".")[0]
	with open(input_file) as csvfile:
		#lsta de titulos
		wiki_articles = list(csv.reader(csvfile))#, delimiter=' ', quotechar='|')
		
		#obtem os dados iniciais
		status = {}

		articles = [article[0] for article in wiki_articles[:3]]
		print(articles)
		dom = WikiPagesCrawler(input_file_name, "2017-10-01T00:00:00Z", "desc", 1, 3)\
				.request_wiki(articles)
		print(dom)

if __name__ == "__main__":
	input_file = sys.argv[1]
	crawler(input_file)
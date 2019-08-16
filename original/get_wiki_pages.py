# -*- coding: utf-8 -*-

from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError
import csv
import time
from datetime import datetime
import requests
from pathlib import Path
import json
import sys
import os

### https://dumps.wikimedia.org/enwiki/latest/
### dumps do banco da wikipedia

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

def request_wiki(articles_array,offset,limit,direction="desc",recursion_depth=0,arq_log=""):
	if(recursion_depth > 5):
		return direction, None
	data_to_request = {"pages":"\n".join(articles_array),
			"offset":offset,
			"dir":direction,
			"limit":limit, # 
			"action":"submit",
			"title":"Special:Export"}

	url_to_request = "https://en.wikipedia.org/w/index.php"
	print(data_to_request["pages"])
	r = requests.post(url_to_request, data=data_to_request)
	print("Requisitando: "+str(len(articles_array))+" páginas")
	#print(r.text)
	try: 
		return parseString(r.text)
	except ExpatError:
		with open(arq_log) as txt:
			txt.write("Error parser:"+",".join(articles_array)+" offset:"+offset+"\n")
		return None

def get_redir_title(dom):
	el = dom.getElementsByTagName("redirect")
	redir_title = None
	if(len(el) > 0):
		redir_title = el[0].attributes["title"].value
	else:
		text_tag = dom.getElementsByTagName("text")
		wiki_text = ""
		if(len(text_tag) > 0 and len(text_tag[0].childNodes) > 0):
			wiki_text = text_tag[0].childNodes[0].data.strip()

		#print("Text wiki: "+wiki_text)		
		#o texto tem algum redirect? 				
		if(wiki_text.startswith("#REDIRECT")):
			open_brackets = wiki_text.find("[[")
			close_brackets = wiki_text.find("]]")
			if(open_brackets > 0 and close_brackets > 0):
				link_string = wiki_text[open_brackets+2:close_brackets]
				redir_title = link_string
	return redir_title

def read_json_crawl(arq):
	with open(arq, 'r') as fp:
		return json.load(fp)

def write_json_crawl(dict_crawl, arq):
	with open(arq, 'w') as fp:
	    json.dump(dict_crawl, fp)

def get_tag_data(dom, tag):
	tag = dom.getElementsByTagName(tag)
	if(len(tag) > 0 and len(tag[0].childNodes) > 0):
		return tag[0].childNodes[0].data.strip()
	return None

# def write_user_rev(str_title,strRedirTitle,dom,rev,fPointer):
# 	#grava: page_id, page_title, page_redir_id, page_redir_title, rev_id, user_id, user_name, rev_timestamp
# 	#page_id_redir = get_tag_data(dom, "id")

# 	rev_id = get_tag_data(rev, "id")
# 	timestamp = get_tag_data(rev, "timestamp")
# 	contributor = rev.getElementsByTagName("contributor")[0]
# 	user_name = get_tag_data(contributor, "username")
# 	user_id = get_tag_data(contributor, "id")
# 	fPointer.write("'"+str(str_title)+"','"+str(strRedirTitle)+"',"+str(rev_id)+","+str(user_id)+",'"+str(user_name)+"','"+str(timestamp)+"'\n")
# 	return timestamp

def write_text(output_dir, str_title, rev):
	text = get_tag_data(rev, "text")
	if text:
		with open(output_dir+"/"+str_title.replace("/","-"),"w") as txt:
			txt.write(text)
		return True
	else:
		return False

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

def get_pages(articles_to_request, offset, limit, arq_log):
	dom = request_wiki(talk_page(articles_to_request),offset=offset,limit=1,arq_log=arq_log)

	pages = dom.getElementsByTagName("page")
	wiki_pages = []

	for page in pages:
		page_id = get_tag_data(page, "id")
		title = get_tag_data(page, "title")
		revision_element = page.getElementsByTagName("revision")[0]
		wiki_text = get_tag_data(revision_element, "text")
		limit = 5
		while is_redirection(wiki_text) and limit:
			redirect_title = redirect(wiki_text)
			dom = request_wiki([redirect_title],offset=offset,limit=1,arq_log=arq_log)
			page = dom.getElementsByTagName("page")[0]
			revision_element = page.getElementsByTagName("revision")[0]
			title = title+"/"+get_tag_data(page, "title")
			wiki_text = get_tag_data(revision_element, "text")
			limit -= 1
		classes = parse_revision_classes(wiki_text)

		wiki_pages.append(WikiPage(page_id, title, classes))
	return wiki_pages

def talk_page(articles):
	return ["Talk:"+article for article in articles]

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


def crawler(input_file):
	input_file_name = input_file.split("/")[-1].split(".")[0]
	with open(input_file) as csvfile:
		#lsta de titulos
		wiki_articles = list(csv.reader(csvfile))#, delimiter=' ', quotechar='|')

		#parametros
		offset = "2017-10-01T00:00:00Z"
		arq_crawl_status = input_file_name+"_crawl_status.json"
		output = input_file_name+"_classes.csv"
		error = input_file_name+"_page_errors.csv"
		articles_per_request = 3

		#obtem os dados iniciais
		dict_crawl = {}
		try:
			dict_crawlNew = read_json_crawl(arq_crawl_status)
			dict_crawl = dict_crawlNew
		except IOError:
			dict_crawl = {"collected_pages":[]}

		collected_articles = set(dict_crawl["collected_pages"])
		articles_to_collect = [article[0] for article in wiki_articles if article[0] not in collected_articles]

		objTime = CheckTime()
		articles_errors = []
		arr_collected_now = []

		while(len(articles_to_collect) > 0):	
			if(len(arr_collected_now) > 0):
				articles_to_collect = list(set(articles_to_collect) - set(arr_collected_now))
				objTime.print_delta("===> Collected articles: "+str(len(arr_collected_now))+") remaining: "+str(len(articles_to_collect)+articles_per_request-len(arr_collected_now)))

			articles_to_request = articles_to_collect[:articles_per_request]
			articles_to_collect = articles_to_collect[articles_per_request:]

			arr_collected_now = []

			wiki_pages = get_pages(articles_to_request,offset=offset,limit=1,arq_log=error)

			with open(output, 'a') as output_pointer, open(error, 'a') as error_pointer:
				csv_writer = csv.writer(output_pointer, delimiter=';',quotechar='"',quoting=csv.QUOTE_NONNUMERIC)

				print("Pages:"+str(len(wiki_pages)))

				for page in wiki_pages:
					csv_writer.writerow([page.id,page.title, page.get_classes()])
					dict_crawl["collected_pages"].append(page.title)
					arr_collected_now.append(page.title)

				write_json_crawl(dict_crawl,arq_crawl_status)

				#caso nao tenha coletado nenhum agora, adicione eles como artigos com erro
				if(len(arr_collected_now) == 0):
					[error_pointer.write(title+";") for title in articles_to_request]
					error_pointer.write("\n")
					articles_errors = articles_to_request
					print("ERROR: Could not collect anything from this list:"+str(articles_to_request))
					time.sleep(30)

			time.sleep(1)

if __name__ == "__main__":
	input_file = sys.argv[1]
	crawler(input_file)

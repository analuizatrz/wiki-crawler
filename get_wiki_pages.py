from xml.dom.minidom import parseString
import csv
import time
from datetime import datetime
import requests
from pathlib import Path
import json
import sys
import os

intFoundRedirect = 0
intFoundRedirectAndAsc = 0
intFoundJustAsc = 0
arrNotFound = []
### https://dumps.wikimedia.org/enwiki/latest/
### dumps do banco da wikipedia

class WikiPage(object):
	def __init__(self, id, title, classes):
		self.id = id
		self.title = title
		self.classes = classes

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
	except xml.parsers.expat.ExpatError:
		with open(arq_log) as txt:
			txt.write("Error parser:"+",".join(articles_array)+" offset:"+offset+"\n")
		return None

# def get_redir_title(dom):
# 	el = dom.getElementsByTagName("redirect")
# 	redir_title = None
# 	if(len(el) > 0):
# 		redir_title = el[0].attributes["title"].value
# 	else:
# 		text_tag = dom.getElementsByTagName("text")
# 		text_wiki = ""
# 		if(len(text_tag) > 0 and len(text_tag[0].childNodes) > 0):
# 			text_wiki = text_tag[0].childNodes[0].data.strip()

# 		#print("Text wiki: "+text_wiki)		
# 		#o texto tem algum redirect? 				
# 		if(text_wiki.lower().startswith("#redirect")):
# 			open_brackets = text_wiki.find("[[")
# 			close_brackets = text_wiki.find("]]")
# 			if(open_brackets > 0 and close_brackets > 0):
# 				link_string = text_wiki[open_brackets+2:close_brackets]
# 				redir_title = link_string
# 	return redir_title

def read_json_crawl(arq):
	with open(arq, 'r') as fp:
		return json.load(fp)
	
def write_json_crawl(dict_crawl, arq):
	with open(arq, 'w') as fp:
	    json.dump(dict_crawl, fp)

def get_tag_data(dom,strTag):
	tag = dom.getElementsByTagName(strTag)
	if(len(tag) > 0 and len(tag[0].childNodes) > 0):
		return tag[0].childNodes[0].data.strip()
	return None

# def write_user_rev(strTitle,strRedirTitle,dom,rev,fPointer):
# 	#grava: page_id, page_title, page_redir_id, page_redir_title, rev_id, user_id, user_name, rev_timestamp
# 	#page_id_redir = get_tag_data(dom, "id")

# 	rev_id = get_tag_data(rev, "id")
# 	timestamp = get_tag_data(rev, "timestamp")
# 	contributor = rev.getElementsByTagName("contributor")[0]
# 	user_name = get_tag_data(contributor, "username")
# 	user_id = get_tag_data(contributor, "id")
# 	fPointer.write("'"+str(strTitle)+"','"+str(strRedirTitle)+"',"+str(rev_id)+","+str(user_id)+",'"+str(user_name)+"','"+str(timestamp)+"'\n")
# 	return timestamp

def write_text(output_dir,strTitle,rev):
	text = get_tag_data(rev, "text")
	if(text):
		with open(output_dir+"/"+strTitle.replace("/","-"),"w") as txt:
			txt.write(text)
		return True
	else:
		return False

def parse_revision_classes(text):
	lines = text.replace("{{","}}").replace("\n","").split("}}")
	classes = []
	for line in lines:
		if "class" in line:
			atributes = line.split("|")
			wiki_project = ""
			wiki_class = "-"
			for idx, atribute in enumerate(atributes):
				atribute_values = atribute.split("=")
				if idx == 0:
					wiki_project = atribute_values[0]
				if atribute_values[0] == "class":
					wiki_class = atribute_values[1]	
			classes.append((wiki_project+": class "+ wiki_class))	
	return classes

def get_pages(dom):
	pages = dom.getElementsByTagName("page")

	wiki_pages = []
	#  [(get_tag_data(page, "title"), page.getElementsByTagName("revision").get_tag_data("text") ) for page in pages]
	for page in pages:
		page_id = get_tag_data(page, "id")
		title = get_tag_data(page, "title")

		revision_element = page.getElementsByTagName("revision")[0]
		text_wiki = get_tag_data(revision_element, "text")
		classes = parse_revision_classes(text_wiki)

		wiki_pages.append(WikiPage(page_id, title, classes))
	return wiki_pages

def talk_pages(articles):
	return [["Talk:"+article[0]] for article in articles]

def crawler(input_file):
	with open(input_file) as csvfile:
		#lsta de titulos
		wiki_articles = list(csv.reader(csvfile))#, delimiter=' ', quotechar='|')
		wiki_articles = talk_pages(wiki_articles)
	
		#parametros
		offset = "2017-10-01T00:00:00Z"
		arq_crawl_status = input_file+"_crawl_status.json"
		output = input_file+"_page_ids.csv"
		error = input_file+"_page_errors.csv"
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
				objTime.print_delta("===> Collected articles: "+str(len(arr_collected_now))+") missing: "+str(len(articles_to_collect)))
				
			articles_to_request = articles_to_collect[:articles_per_request]
			articles_to_collect = articles_to_collect[articles_per_request:]
			
			arr_collected_now = []
			dom = request_wiki(articles_to_request,offset=offset,limit=1,arq_log=error)
			
			wiki_pages = get_pages(dom)

			with open(output, 'a') as output_pointer, open(error, 'a') as error_pointer:
				csv_writer = csv.writer(output_pointer, delimiter=';',quotechar='"',quoting=csv.QUOTE_NONNUMERIC)
				print("Pages:"+str(len(wiki_pages)))
					
				for page in wiki_pages:
					csv_writer.writerow([page.id,page.title, ";".join(page.classes)])

					dict_crawl["collected_pages"].append(page.title)
					arr_collected_now.append(page.title)

				intCollectedNow = len(arr_collected_now)
				write_json_crawl(dict_crawl,arq_crawl_status)
				#caso nao tenha coletado nenhum agora, adicione eles como artigos com erro
				if(intCollectedNow == 0):
					[error_pointer.write(title+";") for title in articles_to_request]
					error_pointer.write("\n")
					articles_errors = articles_to_request
					print("ERROR: Could not collect anything from this list:"+str(articles_to_request))
					time.sleep(30)
			
			time.sleep(1)

if __name__ == "__main__":
	input_file = sys.argv[1]
	crawler(input_file)


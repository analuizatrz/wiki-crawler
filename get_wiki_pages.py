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



class CheckTime(object):
	
	def __init__(self):
		self.time = datetime.now()
		self.sumTime = 0
		self.contDeltas = 0

	def finishTime(self):
	        delta = datetime.now()-self.time
	        self.time = datetime.now()
	        return delta
	def printDelta(self,task):
		delta = self.finishTime()
		self.sumTime += delta.total_seconds()
		self.contDeltas += 1
		print(task+" done in "+str(delta.total_seconds())+" average: "+str(self.sumTime/self.contDeltas))

###multiplas talk pages
#### classes : projeto

### verificar de desc mais antiga dado offset.

def requestWiki(arrArticles,offset,limit,direction="desc",recursionDepth=0,arq_log=""):
	if(recursionDepth>5):
		return direction, None
	dataToResquest = {"pages":"\n".join(arrArticles),
			"offset":offset,
			"dir":direction,
			"limit":limit, # 
			"action":"submit",
			"title":"Special:Export"}

	urlToRequest = "https://en.wikipedia.org/w/index.php"
	print(dataToResquest["pages"])
	r = requests.post(urlToRequest, data=dataToResquest)
	print("Requisitando: "+str(len(arrArticles))+" páginas")
	#print(r.text)
	try: 
		return parseString(r.text)
	except xml.parsers.expat.ExpatError:
		with open(arq_log) as txt:
			txt.write("Error parser:"+",".join(arrArticles)+" offset:"+offset+"\n")
		return None

def get_redir_title(dom):
	el = dom.getElementsByTagName("redirect")
	redirTitle = None
	if(len(el)>0):
		redirTitle = el[0].attributes["title"].value
	else:
		textTag = dom.getElementsByTagName("text")
		textWiki = ""
		if(len(textTag)>0 and len (textTag[0].childNodes)>0):
			textWiki = textTag[0].childNodes[0].data.strip()

		#print("Text wiki: "+textWiki)		
		#o texto tem algum redirect? 				
		if(textWiki.lower().startswith("#redirect")):
			openColchete = textWiki.find("[[")
			fechaColchete = textWiki.find("]]")
			if(openColchete>0 and fechaColchete>0):
				linkStr = textWiki[openColchete+2:fechaColchete]
				redirTitle = linkStr
	return redirTitle

def read_json_crawl(arq):
	with open(arq, 'r') as fp:
		return json.load(fp)
	
def write_json_crawl(dictCrawl, arq):
	with open(arq, 'w') as fp:
	    json.dump(dictCrawl, fp)

def get_tag_data(dom,strTag):
	tag = dom.getElementsByTagName(strTag)
	if(len(tag)>0 and len(tag[0].childNodes)>0):
		return tag[0].childNodes[0].data.strip()
	return None

def write_user_rev(strTitle,strRedirTitle,dom,rev,fPointer):
	#grava: page_id, page_title, page_redir_id, page_redir_title, rev_id, user_id, user_name, rev_timestamp
	#page_id_redir = get_tag_data(dom, "id")

	rev_id = get_tag_data(rev, "id")
	timestamp = get_tag_data(rev, "timestamp")
	contributor = rev.getElementsByTagName("contributor")[0]
	user_name = get_tag_data(contributor, "username")
	user_id = get_tag_data(contributor, "id")
	fPointer.write("'"+str(strTitle)+"','"+str(strRedirTitle)+"',"+str(rev_id)+","+str(user_id)+",'"+str(user_name)+"','"+str(timestamp)+"'\n")
	return timestamp
def write_text(output_dir,strTitle,rev):
	text = get_tag_data(rev, "text")
	if(text):
		with open(output_dir+"/"+strTitle.replace("/","-"),"w") as txt:
			txt.write(text)
		return True
	else:
		return False

if __name__ == "__main__":
	with open(sys.argv[1]) as csvfile:
		#lsta de titulos
		wikiArticles = list(csv.reader(csvfile))#, delimiter=' ', quotechar='|')
	
	
		#parametros
		offset = "2017-10-01T00:00:00Z"
		arq_crawl_status = sys.argv[1]+"_crawl_status.json"
		output = sys.argv[1]+"_page_ids.csv"
		error = sys.argv[1]+"_page_errors.csv"
		articles_per_request = 3

		#obtem os dados iniciais
		dictCrawl = {}
		try:
			dictCrawlNew = read_json_crawl(arq_crawl_status)
			dictCrawl = dictCrawlNew
		except IOError:
			dictCrawl = {"collected_pages":[]}
		
		collected_articles = set(dictCrawl["collected_pages"])
		articles_to_collect = [article[0] for article in wikiArticles if article[0] not in collected_articles]

		objTime = CheckTime()
		articles_errors = []
		arrColectedNow = []
		
		while(len(articles_to_collect)>0):
			#request 1.000 first articles
			
			if(len(arrColectedNow)>0):
				articles_to_collect = list(set(articles_to_collect) - set(arrColectedNow))
				objTime.printDelta("===> Collected articles: "+str(len(arrColectedNow))+") missing: "+str(len(articles_to_collect)))
			
				
			articles_to_request = articles_to_collect[:articles_per_request]
			articles_to_collect = articles_to_collect[articles_per_request:]
			
			#start a new crawling
			arrColectedNow = []
			### limit = 1 , e offset mais antifa na data offset
			### limit revisoes por pagina
			### testes offset se asc ou desc
			dom = requestWiki(articles_to_request,offset=offset,limit=1,arq_log=error)
				
			#get pages
			pages = dom.getElementsByTagName("page")
			rev = pages.getElementsByTagName("revision")[0]
			with open(output, 'a') as output_pointer, open(error, 'a') as error_pointer:
				csvWriter = csv.writer(output_pointer, delimiter=';',quotechar='"',quoting=csv.QUOTE_NONNUMERIC)
				print("Pages:"+str(len(pages)))
					
				for pag in pages:
					#check if it is a redir page. In case it is, put this to request
					page_redir_title = get_redir_title(pag)
					if(page_redir_title):
						articles_to_collect.add(page_redir_title)
					else:	
							 						
						pageId = get_tag_data(pag,"id")
						if(pageId != None):
							pageTitle = get_tag_data(pag,"title")
							csvWriter.writerow([pageId,pageTitle])
							dictCrawl["collected_pages"].append(pageTitle)
							arrColectedNow.append(pageTitle)
				intCollectedNow = len(arrColectedNow)
				write_json_crawl(dictCrawl,arq_crawl_status)
				#caso nao tenha coletado nenhum agora, adicione eles como artigos com erro
				if(intCollectedNow == 0):
					[error_pointer.write(title+";") for title in articles_to_request]
					error_pointer.write("\n")
					articles_errors = articles_to_request
					print("ERROR: Could not collect anything from this list:"+str(articles_to_request))
					time.sleep(30)
			

				
			time.sleep(1)


		


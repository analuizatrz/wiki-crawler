# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
import requests
from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError

class Logger(object):
    # Classe que produz log em arquivo ou no terminal (por default no terminal)
    # Para fazer log em arquivo é necessario passar o filepath
    # Caso nenhuma mensagem seja passada a mensagem nao sera loggada
    # Modos de uso
    #
    # logger1 = Logger("criando arquivo", "log_de_arquivo.txt")
    # logger1.log()

    # logger2 = Logger()
    # logger2.log("problema ao fazer a requisição")

    def __init__(self, message=None, filepath=None):
        self.message = message
        self.filepath = filepath

    def message(self, message):
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

class TextParser(object):
    def __init__(self, logger=None):
        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

    def parse(self, text):
        try: 
            return parseString(text)
        except ExpatError:
            self.logger.log()
        return None
        
class BaseCrawler(object):
    def request(self, url, body=None, logger=None, parser=None):
        r = requests.get(url, data=body)
        if logger:
            logger.log()
        if parser:
            parser.parse(r.text)

class WikiPagesCrawler(BaseCrawler):
    def __init__(self, name, offset, articles_per_request):
        # body of the constructor
        self.offset = "2017-10-01T00:00:00Z"
        self.arq_crawl_status = name+"_crawl_status.json"
        self.output = name+"_classes.csv"
        self.error = name+"_page_errors.csv"
        self.articles_per_request = 3

        self.pages_status_logger = Logger("", self.arq_crawl_status)
        self.error_logger = Logger("", self.arq_crawl_status)
        self.terminal_logger = Logger("", self.arq_crawl_status)
        self.text_parser = TextParser()

    def request_wiki(self, articles_array,offset,limit,direction="desc",recursion_depth=0,arq_log=""):
        url = "https://en.wikipedia.org/w/index.php"
        body = {"pages":"\n".join(articles_array),
			"offset":offset,
			"dir":direction,
			"limit":limit,
			"action":"submit",
			"title":"Special:Export"}
        dom = super().request(url, body, Logger("Requisitando: "+str(len(articles_array))+" páginas", ), )

if  None:
    print("oi")
else:
    print("")
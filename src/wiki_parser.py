from wiki_page import WikiPageWithClass, WikiPageClass
from abc import ABCMeta, abstractmethod

class WikiParser(object, metaclass=ABCMeta):
	"""
	Abstract parser which defines the interface of methods parse and collect
	"""
	@abstractmethod
	def parse(self, HTMLNode):
		"""
		Defines what and how the date from page, a HTMLNode, will be extracted
		"""
		raise NotImplementedError('users must define parse to use this base class')

	@abstractmethod
	def collect(self, wiki_page, csv_writer, status, arr_collected_now):
		"""
		Defines how the data extrated will be used, save and if it will be recursivity
		"""
		raise NotImplementedError('users must define collect to use this base class')

class WikiParserPageWithClass(WikiParser):
	def parse(self, HTMLNode):
		pages = HTMLNode.get_elements("page")
		wiki_pages = []

		for page in pages:
			page_id = page.get_data("id")
			title = page.get_data("title")
			revision_element = page.get_elements("revision")[0]
			wiki_text = revision_element.get_data("text")
			classes = parse_revision_classes(wiki_text)

			wiki_pages.append(WikiPageWithClass(page_id, title, classes))
		return wiki_pages

	def collect(self, wiki_page, csv_writer, status, arr_collected_now):
		csv_writer.writerow(wiki_page.row())
		status["collected_pages"].append(wiki_page.title)
		arr_collected_now.append(wiki_page.title)

class WikiParserCategory(WikiParser):
	def parse(self, HTMLNode):
		pages = HTMLNode.get_elements("page")
		wiki_pages = []

		for page in pages:
			page_id = page.get_data("id")
			title = page.get_data("title")
			revision_element = page.get_elements("revision")[0]
			wiki_text = revision_element.get_data("text")
			classes = parse_revision_classes(wiki_text)

			wiki_pages.append(WikiPageWithClass(page_id, title, classes))
		return wiki_pages

	def collect(self, wiki_page, csv_writer, status, arr_collected_now):
		csv_writer.writerow(wiki_page.row())
		status["collected_wiki_pages"].append(wiki_page.title)
		arr_collected_now.append(wiki_page.title)

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

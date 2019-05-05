from wiki_page import WikiPageClass
import csv

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

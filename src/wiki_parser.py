from wiki_page import WikiPageWithClass, WikiPageClass

def parse_talk_wikipages_with_class(HTMLNode):
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

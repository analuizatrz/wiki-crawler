from wiki_utils import parse_revision_classes
from wiki_page import WikiPageWithClass

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
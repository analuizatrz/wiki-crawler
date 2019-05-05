class WikiPage(object):
	def __init__(self, id, title):
		self.id = id
		self.title = title

	def row(self):
		return [self.id, self.title]

class WikiPageWithClass(WikiPage):
	def __init__(self, id, title, classes):
		super().__init__(id, title)
		self.classes = classes

	def get_classes(self):
		classes_names = [c.wiki_class for c in self.classes]
		return "/".join(classes_names)
		
	def row(self):
		return [self.id, self.title, self.get_classes()]

class WikiPageClass(object):
	def __init__(self, wiki_project, wiki_class):
		self.wiki_project = wiki_project
		self.wiki_class = wiki_class
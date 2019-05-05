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
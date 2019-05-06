from utils import read_first_column, file_name_with_out_extension
from wiki_crawler import WikiPagesCrawler
from wiki_parser import WikiParserPageWithClass, WikiParserCategory
import sys

def wiki_page_class_crawler(input_file_name):
	input_file_name = file_name_with_out_extension(input_file)
	articles = read_first_column(input_file)

	WikiPagesCrawler(input_file_name, "2017-10-01T00:00:00Z", "desc", 1, 3)\
		.request_in_bulks(articles, WikiParserPageWithClass())

def wiki_pages_from_category(input_file):
	input_file_name = file_name_with_out_extension(input_file)
	articles = read_first_column(input_file)

	WikiPagesCrawler(input_file_name, "2017-10-01T00:00:00Z", "desc", 1, 3)\
		.request_in_bulks(articles, WikiParserPageWithClass())

if __name__ == "__main__":
	input_file = sys.argv[1]
	wiki_page_class_crawler(input_file)
	wiki_pages_from_category(input_file)
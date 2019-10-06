from wkutils import match_dates_and_revisions, date_range_monthly
import re

def parse_revisions_info_monthly(response, date_start, date_end):
    """Parses revisions info response returning a discretized list of revisions as if the article were accessed and collected monthly.

    Parameters:
        response (json): raw result of revisions info request
        date_start (str): The start date in the format ISO 8601: 2001-01-15T14:56:00Z
        date_end (str): The end date in the format ISO 8601: 2001-01-15T14:56:00Z

    Returns:
        response (json): revisions as if they were monthly accessed
        is_complete (bool): all dates have been comtemplated
        next_date (str): first date which was not contemplated
    """
    page = list(response["query"]["pages"].values())[0]
    revisions = page["revisions"]
    dates = date_range_monthly(date_end, date_start)

    return match_dates_and_revisions(dates, revisions)


def parse_revision_content(response):
    """Parses revisions content response returning the content

    Parameters:
        response (json): raw result of revisions content request

    Returns:
        content (str): content of revision
    """

    page = list(response["query"]["pages"])[0]
    revision = list(page["revisions"])[0]
   # return (page["pageid"], page["title"], revision["user"], revision["timestamp"], revision["comment"], revision["slots"]["main"]["content"])
    return revision["slots"]["main"]["content"]

def parse_revision_category_content(text):
    result = re.findall(r"(class=(.+?)\||class=(.+?)}|class=(.+?)\n)", text)
    category = result[0][1] if result[0][0][-1:] == '|' else result[0][2] if result[0][0][-1:] == '}' else result[0][3]
    return result, category.strip()

def parse_page_links(response):
    pages = list(response["query"]["pages"].values())
    links = [x["title"] for x in pages[0]["links"]]
    return links
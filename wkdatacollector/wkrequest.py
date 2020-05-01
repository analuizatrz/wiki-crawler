import requests


S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"


def get_titles_from_id(ids):
    """Resquest revision's title by its ids

    Parameters:
        ids (array of str): Ids of articles. example: ["45492", "58791", "171020"]

    Returns:
        response (json): raw result of the request, containing titles
    """
    params = {
        "action": "query",
        "format": "json",
        "pageids": "|".join(ids)
    }

    response = S.get(url=URL, params=params)

    return response.json()


def get_revisions_info(title, date_start, date_end, rvcontinue=None):
    """Resquest revisions info of a wikipedia article by its title, in a period determined by start and end dates

    Parameters:
        title (str): The title of the article
        date_start (str): The start date of querying in the format ISO 8601: 2001-01-15T14:56:00Z
        date_end (str): The end date of querying in the format ISO 8601: 2001-01-15T14:56:00Z

    Returns:
        response (json): raw result of the request
    """
    params = {
        "action": "query",
        "prop": "revisions",
        "format": "json",
        "titles": title,
        "rvlimit": 500,
        "rvprop": "ids|timestamp|user|comment",
        "rvstart": date_start,
        "rvend": date_end,
        "rvdir": "older",
        "redirects": 1
    }
    if rvcontinue is not None:
        params["rvcontinue"] = rvcontinue

    response = S.get(url=URL, params=params)

    return response.json()


def get_revision_content(title, access_date):
    """Resquest revision's content of a wikipedia article by its title and access_data

    Parameters:
        title (str): The title of the article
        access_date (str): The start date of querying in the format ISO 8601: 2001-01-15T14:56:00Z

    Returns:
        response (json): raw result of the request, the page at the specific date or older
    """
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": title,
        "rvprop": "timestamp|user|comment|content|ids",
        "rvslots": "main",
        "formatversion": "2",
        "format": "json",
        "rvlimit": 1,
        "rvstart": access_date,
        "rvdir": "older",
        "redirects": 1
    }

    response = S.get(url=URL, params=params)

    return response.json()

def get_page_links(title, plcontinue=None):
    """Resquest pages referenced by the article with title specified 

    Parameters:
        title (str): The title of the article of which the references will be taken

    Returns:
        response (json): raw result of the request, with titles of referenced pages
    """
    params = {
        "action": "query",
        "prop": "links",
        "format": "json",
        "continue": "||",
        "titles": title,
        "pllimit": "500",
    }
    if plcontinue is not None:
        params["plcontinue"] = plcontinue

    response = S.get(url=URL, params=params)

    return response.json()
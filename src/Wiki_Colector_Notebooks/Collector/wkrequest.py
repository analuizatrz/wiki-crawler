import requests


S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"


def get_titles_from_id(ids):
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

def get_page_links(titles, plcontinue=None):
    params = {
        "action": "query",
        "prop": "links",
        "format": "json",
        "continue": "||",
        "titles": titles,
        "pllimit": "500",
    }
    if plcontinue is not None:
        params["plcontinue"] = plcontinue

    response = S.get(url=URL, params=params)

    return response.json()

if __name__ == "__main__":
    get_titles_from_id_result = get_titles_from_id(ids=["45492", "58791", "171020"])
    print(f"get_titles_from_id: \n{get_titles_from_id_result}")

    get_revisions_info_result = get_revisions_info(
        title="Taiwanese Hokkien",
        date_start="2009-01-03T00:00:00Z",
        date_end="2007-01-03T00:00:00Z"
    )
    print(f"get_tiget_revisions_info: \n{get_revisions_info_result}")

    get_revision_content_result = get_revision_content(
        title = "Zionism",
        access_date = "2008-12-31T19:27:02Z"
    )
    print(f"get_revision_content: \n{get_revision_content_result}")
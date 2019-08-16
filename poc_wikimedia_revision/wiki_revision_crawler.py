import pandas as pd
import json

def read_json(filepath):
    with open(filepath, 'r') as fp:
        return json.load(fp)
    
def date_range_monthly(date_start, date_end):
        return pd.date_range(date_start, date_end, freq='MS').strftime("%Y-%m-%dT%H:%M:%SZ").tolist()[::-1]

def match_dates_and_revisions(dates, revisions):
    """ For each date finds the max possible revision less or equal then the date.
        Assumes that dates and revisions are Ordered descending

    Parameters:
        dates (str): dates
        revisions (objetct): which contain dates 

    Returns:
        result (list): list of tuples
    """

    date_idx = 0
    revision_idx = 0
    result = []

    while date_idx < len(dates) and revision_idx < len(revisions):
        if(revisions[revision_idx]["timestamp"] <= dates[date_idx]):
            result.append(build_revision(dates[date_idx], revisions[revision_idx]))
            date_idx += 1
        else:
            revision_idx += 1

    if(date_idx != len(dates)):
        while date_idx < len(dates):
            result.append({"access" : dates[date_idx], "revision": None})
            date_idx += 1

    return result

def build_revision(date, revision):
    result = {
        "access" : date,
        "revision" : revision
    }

    return result

def parse_revisions_info_monthly(revisions_info_response, date_start, date_end):
    """Parses revisions info response returning a discretized list of revisions as if the article were accessed and collected monthly.
    
    Parameters:
        revisions_info_response (json): raw result of revisions info request

    Returns:
        response (json): revisions as if they were monthly accessed

    """
    page = list(revisions_info_response["query"]["pages"].values())[0]
    revisions = page["revisions"]
    dates = date_range_monthly(date_start, date_end)
    match_dates_and_revisions(dates, revisions)

if __name__ == "__main__":
    date_start = "2017-10-01T00:00:00Z"
    date_end = "2015-10-01T00:00:00Z"

    response = read_json("response.json")
    print(response)
    #revisions_info = parse_revisions_info_monthly(response, date_start, date_end)
    #response
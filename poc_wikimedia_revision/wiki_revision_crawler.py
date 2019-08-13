import pandas as pd

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

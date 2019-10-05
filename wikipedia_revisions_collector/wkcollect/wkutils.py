from pandas import date_range

def match_dates_and_revisions(dates, revisions):
    """ For each date finds the max possible revision less or equal then the date.
        Assumes that dates and revisions are ordered descending

    Parameters:
        dates (str): dates
        revisions (object): which contain dates 

    Returns:
        result (list): list of tuples
        is_complete (bool): all dates have been comtemplated
        next_date: first date which was not contemplated
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

    is_complete = date_idx == len(dates)
    return result, is_complete, None if is_complete else dates[date_idx]


def build_revision(date, revision):
    result = {
        "access": date,
        "revision": revision
    }
    return result

def date_range_monthly(date_start, date_end):
    return date_range(date_start, date_end, freq='MS').strftime("%Y-%m-%dT%H:%M:%SZ").tolist()[::-1]

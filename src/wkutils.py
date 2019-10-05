from pandas import date_range
from datetime import datetime

def date_range_monthly(start, end):
    """ Creates a list of dates between start and end, monthly, ordered descending.
    Start must be older than end, otherwise returns empty list.

    Parameters:
        start (str): start date in the format ISO 8601: 2001-01-15T14:56:00Z
        end (str): end date in the format ISO 8601: 2001-01-15T14:56:00Z

    Returns:
        result (list): list of dates in the format ISO 8601: 2001-01-15T14:56:00Z
    """
    return date_range(start, end, freq='MS').strftime("%Y-%m-%dT%H:%M:%SZ").tolist()[::-1]


def build_revision(date, revision):
    """ Creates dictionary with the values date and revision

    Parameters:
        date (any): date
        revision (any): revision

    Returns:
        result (dict): dictionary with atributtes date and revision
    """
    result = {
        "access": date,
        "revision": revision
    }
    return result


def match_dates_and_revisions(dates, revisions):
    """ For each date finds the max possible revision less or equal then the date.
        Assumes that dates and revisions are ordered descending

    Parameters:
        dates (str): dates in the format ISO 8601: 2001-01-15T14:56:00Z
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

class Timer(object):
    def __init__(self, log):
        self.time = datetime.now()
        self.total_time = 0
        self.delta_count = 0
        self.log = log

    def finish_time(self):
        delta = datetime.now()-self.time
        self.time = datetime.now()
        return delta

    def log_delta(self, task):
        delta = self.finish_time()
        self.total_time += delta.total_seconds()
        self.delta_count += 1
        self.log(task+" done in "+str(delta.total_seconds())+" average: "+str(self.total_time/self.delta_count))

if __name__ == "__main__":
    dates = date_range_monthly(
        start="2007-01-03T00:00:00Z",
        end="2009-01-03T00:00:00Z"
    )
    print(dates)

    revision = build_revision("2007-01-03T00:00:00Z", "revision")
    print(revision)


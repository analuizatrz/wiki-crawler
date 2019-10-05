import unittest
from wkutils import match_dates_and_revisions


class TestWikiParser(unittest.TestCase):

    def call_match_dates_and_revisions(self, dates, revisions):
        r = [{"timestamp": x} for x in revisions]
        return match_dates_and_revisions(dates, r)

    def test_match_dates_revisions(self):
        """
        python -m wiki_revision_crawler_test TestWikiParser.test_match_dates_revisions
        """
        dates = [9, 6, 3, 0]
        revisions = [9, 6, 5, 4, 2, 1]
        actual = self.call_match_dates_and_revisions(dates, revisions)

        self.assertEqual(actual[0]["access"], 9)
        self.assertEqual(actual[1]["access"], 6)
        self.assertEqual(actual[2]["access"], 3)
        self.assertEqual(actual[3]["access"], 0)

        self.assertEqual(actual[0]["revision"]["timestamp"], 9)
        self.assertEqual(actual[1]["revision"]["timestamp"], 6)
        self.assertEqual(actual[2]["revision"]["timestamp"], 2)
        self.assertEqual(actual[3]["revision"], None)

        dates = [8, 5, 2, 1]
        revisions = [9, 6, 5, 4, 2, 1]
        actual = self.call_match_dates_and_revisions(dates, revisions)

        self.assertEqual(actual[0]["access"], 8)
        self.assertEqual(actual[1]["access"], 5)
        self.assertEqual(actual[2]["access"], 2)
        self.assertEqual(actual[3]["access"], 1)

        self.assertEqual(actual[0]["revision"]["timestamp"], 6)
        self.assertEqual(actual[1]["revision"]["timestamp"], 5)
        self.assertEqual(actual[2]["revision"]["timestamp"], 2)
        self.assertEqual(actual[3]["revision"]["timestamp"], 1)

        dates = [9, 8, 7]
        revisions = [6, 5]
        actual = self.call_match_dates_and_revisions(dates, revisions)

        self.assertEqual(actual[0]["access"], 9)
        self.assertEqual(actual[1]["access"], 8)
        self.assertEqual(actual[2]["access"], 7)

        self.assertEqual(actual[0]["revision"]["timestamp"], 6)
        self.assertEqual(actual[1]["revision"]["timestamp"], 6)
        self.assertEqual(actual[2]["revision"]["timestamp"], 6)

        dates = [9, 8, 7]
        revisions = [11, 10]
        actual = self.call_match_dates_and_revisions(dates, revisions)

        self.assertEqual(actual[0]["access"], 9)
        self.assertEqual(actual[1]["access"], 8)
        self.assertEqual(actual[2]["access"], 7)

        self.assertEqual(actual[0]["revision"], None)
        self.assertEqual(actual[1]["revision"], None)
        self.assertEqual(actual[2]["revision"], None)


if __name__ == '__main__':
    unittest.main()

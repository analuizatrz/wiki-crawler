import unittest
from wkparse import parse_revision_category_content


class WkparserTest(unittest.TestCase):
    def test_default_content(self):
        """
        python -m wiki_revision_crawler_test TestWikiParser.test_match_dates_revisions
        """
        input = "{{class=A}}"
        raw, actual =  parse_revision_category_content(input)
        expected = "A"
        self.assertEqual(expected, actual)

    def test_content_with_pipe(self):
        """
        python -m wiki_revision_crawler_test TestWikiParser.test_match_dates_revisions
        """
        input = "{{class=A|sadad}}"
        raw, actual =  parse_revision_category_content(input)
        expected = "A"
        self.assertEqual(expected, actual)

    def test_content_ending_with_pipe(self):
        """
        python -m wiki_revision_crawler_test TestWikiParser.test_match_dates_revisions
        """
        input = "{{class=A|}}"
        raw, actual =  parse_revision_category_content(input)
        expected = "A"
        self.assertEqual(expected, actual)
        
    def test_content_ending_with_linebreak(self):
        """
        python -m wiki_revision_crawler_test TestWikiParser.test_match_dates_revisions
        """
        input = "{{class=A\n|}}"
        raw, actual =  parse_revision_category_content(input)
        expected = "A"
        self.assertEqual(expected, actual)

    def test_content_ending_with_enter(self):
        """
        python -m wiki_revision_crawler_test TestWikiParser.test_match_dates_revisions
        """
        input = "{{class=A }}"
        raw, actual =  parse_revision_category_content(input)
        expected = "A"
        self.assertEqual(expected, actual)

    def test_content_ending_with_pipe1(self):
        """
        python -m wiki_revision_crawler_test TestWikiParser.test_match_dates_revisions
        """
        input = "{{WikiProject Animation|class=A|importance=|american-animation=yes|"
        raw, actual =  parse_revision_category_content(input)
        expected = "A"
        self.assertEqual(expected, actual)

    def test_content_ending_with_pipe2(self):
        """
        python -m wiki_revision_crawler_test TestWikiParser.test_match_dates_revisions
        """
        input = "tatus=FFAC\n}}\n{{WikiProjectBanners\n|1={{WikiProject Plants|class=B|importance=Mid}}\n|2={{WPBiography|living=no|class=B|priority=Mid\n|n"
        raw, actual =  parse_revision_category_content(input)
        expected = "B"
        self.assertEqual(expected, actual)

    def test_content_ending_with_le(self):
        """
        python -m wiki_revision_crawler_test TestWikiParser.test_match_dates_revisions
        """
        input = "{{class=stub<!-- B-Class checklis}}"
        raw, actual =  parse_revision_category_content(input)
        expected = "stub"
        self.assertEqual(expected, actual)

        
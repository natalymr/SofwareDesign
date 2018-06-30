from unittest import TestCase

from grep import Grep, GrepMatch


class TestGrep(TestCase):

    def test_simple_regexp_works_for_single_occurrence(self):
        grep = Grep(pattern="a")

        self.assertEqual(grep.match("abc"), [GrepMatch(0, 1)])
        self.assertEqual(grep.match("bac"), [GrepMatch(1, 2)])
        self.assertEqual(grep.match("bca"), [GrepMatch(2, 3)])

    def test_simple_regexp_works_for_many_occurrences(self):
        grep = Grep(pattern="cat")

        self.assertEqual(
            grep.match("cat catty cat"),
            [GrepMatch(0, 3), GrepMatch(4, 7), GrepMatch(10, 13)]
        )

    def test_complex_regexp_works_on_single_occurrence(self):
        grep = Grep(pattern="ab+c{3}")

        self.assertEqual(grep.match("abccc"), [GrepMatch(0, 5)])
        self.assertEqual(grep.match("accc"), [])
        self.assertEqual(grep.match("abcc"), [])

    def test_complex_regexp_works_on_many_occurences(self):
        grep = Grep(pattern="a{2,3}bc+")

        self.assertEqual(
            grep.match("aabc aaabccccc aab"),
            [GrepMatch(0, 4), GrepMatch(5, 14)]
        )

    def test_ignore_case_flag_works(self):
        grep = Grep(pattern="aaa", ignore_case=True)

        self.assertEqual(
            grep.match("aAa AAA aaa"),
            [GrepMatch(0, 3), GrepMatch(4, 7), GrepMatch(8, 11)]
        )

    def test_whole_word_flag_works(self):
        grep = Grep(pattern="word", whole_word=True)

        self.assertEqual(
            grep.match("word notword wordnot word, word"),
            [GrepMatch(0, 4), GrepMatch(21, 25), GrepMatch(27, 31)]
        )
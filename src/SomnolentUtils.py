#!/usr/bin/env python

"""
SomnolentUtils provides utilities for interfacing with somnolentworks.com
in various ways.  Most notably, it provides an API for easy retrieval of story
content.
"""

import re
from itertools import product
from random import randint, choice
from urllib.request import urlopen
from html.parser import HTMLParser
from html.entities import name2codepoint

SOMNOLENT_URL = 'http://www.somnolentworks.com/'

class SomnolentAPI:
    """ An API for accessing tweet-ready content from somnolentworks.com """

    NEGATIVE_LOOKAHEAD = [ # Patterns that are allowed to be after a period.

        ] #+ list('0123456789')

    NEGATIVE_LOOKBEHIND = [ # Patterns that are allowed to preceed a period.
        'mr', 'ms', 'mrs', 'dr', 'sr', 'sra'
        ] #+ list('bcdefghjklmnopqrstuvwxyz')

    def __init__(self):
        self.num_stories = SomnolentLatestStoryParser().get_story_number()
        self._lookahead_pattern = self._get_lookahead_pattern()
        self._lookbehind_pattern = self._get_lookbehind_pattern()

    def get_random_story_content(self):
        """ Returns a tuple of (story title, story sentence body) """
        story_id = self._get_random_story_number()
        story = SomnolentStory(SOMNOLENT_URL + str(story_id) + '.html')
        return (story.get_title(), self._parse_sentence(story.get_story()))

    def _parse_sentence(self, story):
        return choice(re.findall(
            '[a-zA-Z0-9]+.*?' + self._lookbehind_pattern +
            '[.?!]' + self._lookahead_pattern,
            story
            ))

    def _get_random_story_number(self):
        return randint(1, self.num_stories)

    def _get_lookahead_pattern(self):
        return ''.join(map(lambda word: '(?!' + word + ')',
            self._generate_word_case_permutations(self.NEGATIVE_LOOKAHEAD)
            ))

    def _get_lookbehind_pattern(self):
        return ''.join(map(lambda word: '(?<!' + word + ')',
            self._generate_word_case_permutations(self.NEGATIVE_LOOKBEHIND)
            ))

    def _generate_word_case_permutations(self, words):
        """
        words: A list of strings to be case-permuted.
        Returns a list of strings where all permutations of capitalization are
        present.
        For example: ['me', 'I'] -> ['ME', 'Me', 'mE', 'me', 'I', 'i'].
        """
        result = []
        for word in words:
            result += list(
                ''.join(w) for w in product(*zip(word.lower(), word.upper()))
                )
        return result

class SomnolentStory:
    """ A representation of a story as displayed on somnolentworks.com. """

    def __init__(self, url):
        """
        url: A string representing the url where the story lives.
        """
        res = urlopen(url)
        parser = SomnolentHTMLParser()
        parser.feed(str(res.read()))
        (self.title, self.story) = parser.get_story()

    def get_title(self):
        """ Returns string representing the title of the story. """
        return self.title

    def get_story(self):
        """ Returns string representing the story. """
        return self.story

class SomnolentHTMLParser(HTMLParser):
    """ A parser designed to parse story pages of somnolentworks.com. """

    TITLE_TAG = 'title'
    STORY_TAG = 'p'

    def __init__(self):
        super().__init__()
        self.parsedTitle = ''
        self.parsedStory = ''
        self._state = None

    def handle_starttag(self, tag, attrs):
        if (tag in (self.TITLE_TAG, self.STORY_TAG) and attrs == []):
            self._state = tag
        else:
            self._state = None

    def handle_endtag(self, tag):
        self._state = None

    def handle_data(self, data):
        self._write_data(data)

    def handle_entityref(self, name):
        self._write_data(chr(name2codepoint[name]))

    def handle_charref(self, name):
        if name.startswith('x'):
            self._write_data(chr(int(name[1:], 16)))
        else:
            self._write_data(chr(int(name)))

    def get_story(self):
        """
        Returns a tuple where the first element is a string representing the
        title of the parsed story, and the second element is a string
        representing the story itself.
        """
        return (self.parsedTitle, self.parsedStory)

    def _write_data(self, data):
        data = re.sub('\\\\n|\\\\t|\\\\r', '', data) # Weird escaped whitespace.
        if self._state == self.TITLE_TAG:
            self.parsedTitle += data
        elif self._state == self.STORY_TAG:
            self.parsedStory += data

class SomnolentLatestStoryParser(HTMLParser):
    """ A parser that provides the latest somnolent story number. """

    def __init__(self):
        super().__init__()
        self.latest = None

    def get_story_number(self):
        """ Returns the most recently written story number. """
        res = urlopen(SOMNOLENT_URL)
        self.feed(str(res.read()))
        if self.latest is None:
            raise SomnolentParseException('Could not parse latest story')
        return self.latest

    def handle_starttag(self, tag, attrs):
        if self.latest is None and tag == 'a':
            for (name, val) in attrs: # Loop through list and find first url
                                      # with numbers in it
                if (name == 'href' and
                    re.search(SOMNOLENT_URL + '\d+\.html', val)):
                    self.latest = int(re.search('\d+', val).group(0))

class SomnolentParseException(Exception):
    def __init__(self, value):
        self.value = value

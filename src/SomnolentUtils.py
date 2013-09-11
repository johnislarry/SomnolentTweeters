#!/usr/bin/env python

"""
SomnolentUtils provides utilities for interfacing with somnolentworks.com
in various ways.  Most notably, it provides an API for easy retrieval of story
content.
"""

from urllib.request import urlopen
from html.parser import HTMLParser
from html.entities import name2codepoint

TWEET_CHAR_MAX = 140
SOMNOLENT_URL = 'http://www.somnolentworks.com/'
EXTENSION = '.html'

class SomnolentAPI:
    """ An API for accessing tweet-ready content from somnolentworks.com """



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
        if self._state == self.TITLE_TAG:
            self.parsedTitle += data.strip()
        elif self._state == self.STORY_TAG:
            self.parsedStory += data.strip()

class SomnolentLatestStoryParser(HTMLParser)
    """ A parser that provides the latest somnolent story number. """
    def __init__(self):
        super().__init__()
        self.latest = None

    def get_latest_story_number(self):
        """ Returns the most recently written story number. """
        res = urlopen(SOMNOLENT_URL)
        self.feed(str(res.read()))
        if self.latest is None:
            raise SomnolentParseException('Could not parse latest story')
        return self.latest

    def handle_starttag(self, tag, attrs):

    def handle_endtag(self, tag):

    def handle_data(self, data):

class SomnolentParseException(Exception):
    def __init__(self, value):
        self.value = value

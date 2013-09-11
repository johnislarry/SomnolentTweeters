#!/usr/bin/env python

"""
SomnolentUtils provides utilities for interfacing with somnolentworks.com
in various ways.  Most notably, it provides an API for easy retrieval of story
content.
"""

from urllib.request import urlopen
from html.parser import HTMLParser

class SomnolentStory:
    """ A representation of a story as displayed on somnolentworks.com. """

    def __init__(self, url):
        """
        url: A string representing the url where the story lives.
        """
        res = urlopen(url)
        parser = SomnolentHTMLParser()
        parser.feed(str(res.read()))
        story = parser.get_story()

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

    def handle_data(self, data):
        if self._state == self.TITLE_TAG:
            self.parsedTitle += data
        elif self._state == self.STORY_TAG:
            self.parsedStory += data

    def get_story(self):
        """
        Returns a tuple where the first element is a string representing the
        title of the parsed story, and the second element is a string
        representing the story itself.
        """
        return (self.parsedTitle, self.parsedStory)

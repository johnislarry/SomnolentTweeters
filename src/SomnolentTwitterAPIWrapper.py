#!/usr/bin/env python

"""
SomnolentTwitterAPIWrapper provides a wrapper around the python twitter tools
package.
"""

import os

from twitter import oauth_dance, read_token_file, Twitter, OAuth

class SomnolentTwitterWrapper:

    APP_NAME = 'SomnolentTweeters'
    CONSUMER_KEY = 'HUSYsjnkSi2AxQeXxnnMBQ'
    TWITTER_CREDS = os.path.expanduser('~/.somnolent_credentials')

    def __init__(self, consumer_secret):
        self._consumer_secret = consumer_secret
        self.twitter = self.authenticate()

    def authenticate(self):
        """ Authenticates with twitter app and returns a Twitter object. """
        if not os.path.exists(self.TWITTER_CREDS):
            oauth_dance(
                    self.APP_NAME,
                    self.CONSUMER_KEY,
                    self._consumer_secret,
                    self.TWITTER_CREDS
                    )
        oauth_token, oauth_secret = read_token_file(self.TWITTER_CREDS)
        return Twitter(auth=OAuth(
            oauth_token, oauth_secret, self.CONSUMER_KEY, self._consumer_secret
            ))

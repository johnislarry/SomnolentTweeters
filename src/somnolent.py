#!/usr/bin/env python

"""
A command line script to tweet a randomly selected sentence from
somnolentworks.com.  User must pass in the consumer secret key.
"""

import sys
import re

from SomnolentUtils import SomnolentAPI
from SomnolentTwitterAPIWrapper import SomnolentTwitterWrapper

MAX_TRIES = 5
MAX_TWEET_LENGTH = 140

try:
    key = sys.argv[1]
except IndexError:
    sys.exit('You need to pass in the consumer secret key!')

def hashtagify(s):
    """
    Takes in a string and returns its hashtagified version.  That is to say,
    the string with whitespace, periods, and apostrophes removed and a '#'
    prepended to it.
    """
    return re.sub(
        '\.|\'',
        '',
        '#' + ''.join(map(lambda x: x.capitalize(), s.split()))
        )

def main():
    """
    Attempt to tweet a randomly chosen sentence from somnolentworks.com, and
    a hashtagified form of the title.  If the combined character count of both
    of these is greater than 140, then attempt to just tweet the random
    sentence.  If this character count alone is greater than 140, randomly pick
    a new sentence and repeat the previous procedure.
    """
    api = SomnolentAPI()
    twitter = SomnolentTwitterWrapper(key).twitter

    tries = 0
    while tries < MAX_TRIES:
        tries += 1
        title, sentence = api.get_random_story_content()
        tweet = sentence + ' ' + hashtagify(title)
        if len(tweet) <= MAX_TWEET_LENGTH:
            break
        elif len(sentence) <= MAX_TWEET_LENGTH:
            tweet = sentence
            break
    else:
        sys.exit('Failed to find a valid sentence after %s tries' % MAX_TRIES)

    twitter.statuses.update(status=tweet)

main()

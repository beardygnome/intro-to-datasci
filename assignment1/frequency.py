#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def main():
    """(NoneType) -> NoneType

    Run the program
    """
    tweet_file = open(sys.argv[1])
    tweet_texts = []

    for line in tweet_file:
        tweet_text == process_tweet(line)

        if tweet_text:
            tweet_texts.add(tweet_text)


def process_tweets(tweet):
    """(str) -> str

    Return the tweet text for the tweet
    """

    tweet = json.loads(tweet)
    tweet_text = None

    if not "delete" in tweet:
        tweet_text = tweet["text"]

    return tweet_text


if __name__ == "__main__":
    main()

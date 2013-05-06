#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys

def main():
    """(NoneType) -> NoneType

    Run the program.
    """

    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    sentiments = process_sentiments(sent_file)

    i = 0
    for line in tweet_file:
        if i < 20:
            i += 1
        else:
            break

        score = process_tweet(line, sentiments)

        print score


def process_sentiments(scores):
    """(File) -> dict(str, float)

    Take string, score pairs from scores and return a dictionary of
    strings and floats.
    """

    dictionary = {}

    for line in scores:
        string, score = line.strip().split('\t')
        dictionary[string] = float(score)

    return dictionary


def process_tweet(tweet, scores):
    """(File, dict(str, float)) -> (str, float

    Return the state and the overall score of each tweet.
    """

    sentiment = 0.0

    tweet = json.loads(tweet)


    if not "delete" in tweet:
        tweet_text = tweet["text"]

        for word in tweet_text.split():
            if word in scores:
                sentiment += scores[word]

    return sentiment


if __name__ == '__main__':
    main()

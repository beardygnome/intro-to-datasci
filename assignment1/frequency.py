#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys

def main():
    """(NoneType) -> NoneType

    Run the program
    """
    tweet_file = open(sys.argv[1])
    tweet_texts = []

    for line in tweet_file:
        tweet_text = process_tweet(line)

        if tweet_text:
            tweet_texts.append(tweet_text)

    #print tweet_texts

    words = {}
    tot_num_words = 0.0

    for text in tweet_texts:
        for word in text.split():
            tot_num_words += 1.0

            if word in words:
                words[word] += 1.0
            else:
                words[word] = 1.0

    for word in words:
        words[word] = words[word] / tot_num_words

    i = 0
    for word in words:
        #if i < 20:
        #    i += 1
        #else:
        #    break

        print word, words[word]



def process_tweet(tweet):
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

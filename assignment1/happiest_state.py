#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys

def get_tweet_suitability(tweet):
    """(dict(str, str)) -> (bool, str)

    Return True and the state code if the tweet is suitable for analysis,
    otherwise False and the state code, if appropriate.
    """

    result = False
    state = ""

    if not "delete" in tweet:
        place = tweet["place"]

        if not place == None:
            country_code = place["country_code"]

            if country_code == "US":
                full_name = place["full_name"]
                city, state = full_name.split(",")
                state = state.lstrip()

                if not (state == "US" or len(state) > 2):
                    result = True

    return result, state


def main():
    """(NoneType) -> NoneType

    Run the program.
    """

    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    sentiments = process_sentiments(sent_file)

    i = 0
    states = {}

    for line in tweet_file:
        #if i < 5000:
        #    i += 1
        #else:
        #    break

        tweet = json.loads(line)
        tweet_suitable, state = get_tweet_suitability(tweet)
        sentiment = 0.0

        if tweet_suitable:
            sentiment = process_tweet(tweet, sentiments)

            if state in states:
                states[state] += sentiment
            else:
                states[state] = sentiment

    state_list = []

    for state in states:
        state_list.append([states[state], state])

    state_list.sort(reverse=True)

    print state_list[0][1].encode("utf-8")

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
    """(dict(str, str), dict(str, float)) -> float

    Return the state and the overall score of each tweet.
    """

    place = ""
    sentiment = 0.0

    tweet_text = tweet["text"]

    for word in tweet_text.split():
        if word in scores:
            sentiment += scores[word]

    return sentiment


if __name__ == '__main__':
    main()

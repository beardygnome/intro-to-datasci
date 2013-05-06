#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import urllib

search_url = "http://search.twitter.com/search.json?q="


def main():
    """(NoneType) -> int

    Run the program.  Return 0 if there are no errors, otherwise 1
    """
    err = False

    keyword = sys.argv[1] #"experian"
    pages = int(sys.argv[2]) #10

    (twitter_search(keyword))

    for i in range(1, pages + 1):
        #print i
        data = twitter_search(keyword, i)
        process_results(data)


    return 0


def process_results(search_results):
    """(dict) -> NoneType

    Print the text for each tweet in search_results
    """

    results = search_results["results"]

    #for key in results[0]: print key

    for tweet in results:
        print tweet["text"]



def twitter_search(search_term, page_num = None):
    """(str, int) -> dict

    Search Twitter using search_term and page_num.  Returns the JSON object
    encoded as a python dictionary.
    """

    url = search_url + search_term

    if page_num:
        url += "&page=" + str(page_num)

    return json.load(urllib.urlopen(url))


if __name__ == '__main__':
    main()

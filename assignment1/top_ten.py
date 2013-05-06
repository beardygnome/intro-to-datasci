#!/usr/bin/ev python
# -*- coding: utf-8 -*-

import json
import sys

def main():
	"""(NoneType) -> NoneType

	Run the program.
	"""

	tweet_file = open(sys.argv[1])

	i = 0

	hashtag_dict = {}

	for line in tweet_file:
		tweet = json.loads(line)

		if "entities" in tweet:
			entities = tweet["entities"]

			if "hashtags" in entities and len(entities["hashtags"]) > 0:
				hashtags = entities["hashtags"]

				for hashtag in hashtags:
					hashtag_text = hashtag["text"]

					if hashtag_text in hashtag_dict:
						hashtag_dict[hashtag_text] += 1.0
					else:
						hashtag_dict[hashtag_text] = 1.0

				if i < 200:
					i += 1
				else:
					break

	hashtag_list = []

	for hashtag in hashtag_dict:
		hashtag_list.append([hashtag_dict[hashtag], hashtag])

	hashtag_list.sort(reverse=True)

	for i in range(10):
		print hashtag_list[i][1], hashtag_list[i][0]


if __name__ == "__main__":
	main()

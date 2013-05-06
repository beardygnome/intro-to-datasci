import json
import sys

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))


def get_new_words(processed_tweet, scores, new_words):
    """((str, float), dict(str, float), dict(str, list of float) -> NoneType

    Collect words in tweet that don't appear in scores and assign them
    to new_words, along with a count of the number of times they appear and
    their total tweet score.
    """

    tweet_text, tweet_score, average_score = processed_tweet
    tweet_words = tweet_text.split()

    for word in tweet_words:
        if not word in scores:
            if word in new_words:
                new_words[word][0] += 1.0
                new_words[word][1] += average_score
            else:
                new_words[word] = [1.0, average_score]


def main():
    """(NoneType) -> NoneType

    Run the program
    """

    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #hw()
    #lines(sent_file)
    #lines(tweet_file)

    sentiments = process_sentiments(sent_file)
    new_words = {}

    for line in tweet_file:

        processed_tweet = process_tweet(line, sentiments)
        get_new_words(processed_tweet, sentiments, new_words)

    new_word_scores = process_new_words(new_words)

    for key in new_word_scores:
        print key.encode("utf-8"), (new_word_scores[key])


def process_new_words(new_words):
    """(dict(str, list of float) -> dict(str, float)

    Calculate the overall score for each new word
    """

    new_word_scores = {}

    for key in new_words:
        new_word_scores[key] = new_words[key][1] / new_words[key][0]

    return new_word_scores


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
    """(str, dict(str, float)) -> (str, float, int)

    Return the text overall score and average score of each tweet.
    """

    tweet_text = ""
    sentiment = 0.0
    words_used = 0
    average_score = 0.0

    tweet = json.loads(tweet)


    if not "delete" in tweet:
        tweet_text = tweet["text"]

        for word in tweet_text.split():
            if word in scores:
                sentiment += scores[word]
                words_used += 1

        if not words_used == 0:
            average_score = sentiment / words_used

    return (tweet_text, sentiment, average_score)


if __name__ == '__main__':
    main()

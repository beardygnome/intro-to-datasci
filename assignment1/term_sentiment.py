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

    tweet_text, tweet_score = processed_tweet
    tweet_words = tweet_text.split()
    tweet_wordcount = len(tweet_words)


    for word in tweet_words:
        if not word in scores:
            new_score = tweet_score / tweet_wordcount

            if word in new_words:
                new_words[word][0] += 1.0
                new_words[word][1] += new_score
            else:
                new_words[word] = [1.0, new_score]



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

    i = 0
    for line in tweet_file:
        if i < 20:
            i += 1
        else:
            break

        get_new_words(process_tweet(line, sentiments), sentiments, new_words)

    for key in new_words:
        print key + " : " + str(new_words[key])#[0], new_words[key][1]


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
    """(str, dict(str, float)) -> (str, float)

    Return the overall score of each tweet.
    """

    sentiment = 0.0

    tweet = json.loads(tweet)


    if not "delete" in tweet:
        tweet_text = tweet["text"]

        for word in tweet_text.split():
            if word in scores:
                sentiment += scores[word]

        return (tweet_text, sentiment)
    else:
        return ("", sentiment)


if __name__ == '__main__':
    main()

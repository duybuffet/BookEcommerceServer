# -*- coding: utf-8 -*-
import requests
import re
import threading
import time
import math
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag


__author__ = 'Duy'

wnl = WordNetLemmatizer()


def load_stopwords_set(filename):
    f = open(filename, 'r')
    return set(f.read().split("\n"))

stopword_set = load_stopwords_set('stopwords.txt')


def extract_snippet(keyword):
    r = requests.get("https://en.wikipedia.org/w/api.php?action=opensearch&search=%s&format=json" % keyword.strip())
    result = r.json()
    if len(result[1]) > 1:
        snippet_without_schar = re.sub(r"[^\x00-\x7F]+", '', result[2][0])
        snippet_without_pronunciation = re.sub(r"(\/[\w ]+\/)", '', snippet_without_schar)
        snippet_without_punctuation = re.sub(r"[\(\)\;\.\,]+", '', snippet_without_pronunciation)
        return re.sub(r"[ ]+", ' ', snippet_without_punctuation)
    return ""


def remove_stopwords(snippet):
    set_snippet, result = set(snippet.split(" ")), []
    [result.append(x.lower()) for x in set_snippet if x.lower() not in stopword_set]
    return result


class GetRemovedStopWordSetThread(threading.Thread):
    def __init__(self, keyword, result):
        threading.Thread.__init__(self)
        self.keyword = keyword
        self.result = result

    def run(self):
        self.result.append(remove_stopwords(extract_snippet(self.keyword)))


def similarity_measure(keyword1, keyword2, algorithm):
    result = []
    # Create new threads
    thread1, thread2 = GetRemovedStopWordSetThread(keyword1, result), GetRemovedStopWordSetThread(keyword2, result)
    # Start new Threads
    thread1.start()
    thread2.start()
    # Join thread
    thread1.join()
    thread2.join()

    if len(result) == 2:
        set1, set2 = [], []
        [set1.append(wnl.lemmatize(i, j[0])) if j[0] in ['a', 'n', 'v'] else set1.append(wnl.lemmatize(i)) for i,j in pos_tag(result[0])]
        [set2.append(wnl.lemmatize(i, j[0])) if j[0] in ['a', 'n', 'v'] else set2.append(wnl.lemmatize(i)) for i,j in pos_tag(result[1])]
        intersec_len = len(set(set1).intersection(set(set2)))
        set1_len, set2_len = len(set1), len(set2)
        print("intersec set : %s" % set(set1).intersection(set(set2)))

        algorithm = algorithm.lower()
        if algorithm == "jaccard":
            return intersec_len / float(set1_len + set2_len - intersec_len)
        elif algorithm == "simple":
            return intersec_len
        elif algorithm == "overlap":
            return intersec_len / float(min(set1_len, set2_len))
        elif algorithm == "dice":
            return intersec_len / float(set1_len + set2_len)
        elif algorithm == "cosine":
            return intersec_len / float((math.sqrt(set1_len) * math.sqrt(set2_len)))
        else:
            return 0
    else:
        return 0

start = time.clock()
print similarity_measure('tim cook', 'steve jobs', "jaccard")

# txt = "freaking math people hardest crushes"
# print [wnl.lemmatize(i,j[0].lower()) if j[0].lower() in ['a','n','v'] else wnl.lemmatize(i) for i,j in pos_tag(word_tokenize(txt))]
print "Spending time : %s" % (time.clock() - start)
# print pos_tag(["crawls", "hello"])

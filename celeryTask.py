from celery import Celery
import json
import os
import re
import json
import itertools
import collections


app = Celery('celery', broker='amqp:localhost', backend='rpc://')


def clean(txt):
    # remove urls and emojies
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())


@app.task
def freq():
    path = "./data/"
    files = os.listdir(path)
    temp = {}
    num = 0
    for file in files:
        words = []
        with open(path + os.sep + file, 'r') as f:
            print("Processing file: " + f.name)
            for line in f:
                if not line.isspace():
                    # ignore retweets
                    if "retweeted_status" in json.loads(line):
                        continue
                    else:
                        # unique tweets
                        num += 1
                        cleanTxt = clean(json.loads(line)["text"])
                        words.append(cleanTxt.lower().split())
        flat_words = list(itertools.chain(*words))

        countsAll = collections.Counter(flat_words)

        pronouns = 'han', 'hon', 'den', 'det', 'denna', 'denne', 'hen'
        counts = {}
        for p in pronouns:
            if p in countsAll:
                counts[p] = countsAll[p]

            else:
                counts[p] = 0

        if temp == {}:
            temp = counts
        else:
            for k in temp.keys():
                temp[k] = temp.get(k) + counts.get(k)

    result = []
    for i in list(temp.values()):
        result.append(i / num)
        print(i)
    print(num)
    print(list(temp.values()))
    print(result)

    with open('result.json', 'w') as j:
        jf = json.dump(temp, j)

    with open('result2.json', 'w') as j:
        normalizations = json.dump(result, j)

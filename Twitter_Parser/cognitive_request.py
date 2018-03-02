import httplib, urllib, base64
import sys
import json
import csv
import re
from tabulate import tabulate
import time

t0 = time.time()

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'abbd31b498274e9d8d605be7621e81ad',
}

params = urllib.urlencode({
    # Request parameters
    'numberOfLanguagesToDetect': '1',
})

allTweetsSentiments = csv.reader(open('./../app/data_files/testing_file.csv', 'rb'), delimiter = '|')
table_header = ['Tweet', 'Predicted_ Sentiment', 'Actual Sentiment']
table_data = []
correct_prediction = 0.000
rows_count = 0.000

for rows in allTweetsSentiments:

    text = rows[1]
    actual_sentiment = rows[0]
    quoted_text = text.replace('\'', '\\\'')

    body = "{'documents': [{'id': 'test001',\'text\':'"+quoted_text+"'}]}"
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/text/analytics/v2.0/keyPhrases?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    d= json.loads(data)
    s1 = d['documents'][0]
    keyphrases = s1['keyPhrases']
    print 'Most significant phrases:'
    for member in keyphrases:
        print ' '+member

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/text/analytics/v2.0/sentiment?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        d= json.loads(data)
        s1 = d['documents'][0]
        sentimet_score = s1['score']
        if sentimet_score >= 0.5:
            predicted_sentiment = 'positive'
        else:
            predicted_sentiment = 'negative'

        table_data.append((text, predicted_sentiment, actual_sentiment))
        rows_count = rows_count + 1
        if predicted_sentiment == actual_sentiment:
            correct_prediction = correct_prediction + 1

    except Exception as e:
        print e

t1 = time.time()
time_taken = t1 - t0
time_minute, time_second = time_taken // 60, time_taken % 60

accuracy = float(correct_prediction/rows_count) * 100
print 'Cognitive Text Classification Result:\nAccuracy = ' + str(accuracy) + '%\nTime taken: '+str(time_minute)+' mins '+str(time_second)+' secs\n\n'
print tabulate(table_data, table_header)




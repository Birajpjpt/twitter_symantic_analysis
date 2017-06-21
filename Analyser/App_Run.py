from flask import Flask, jsonify, request
from Analyser.run import run

app = Flask(__name__)
version = '/api/v1.0'

@app.route('/')
def welcome():
    return 'OK'

@app.route(version + '/svm', methods=['GET'])
def svm_predict():
    tweet = request.args.get('word')
    sentiment , positive_probability, negative_probability,  keywords = run().SVMtestSingleTweet(tweet)
    svm_classification = [
        {   'Actual-Tweet': tweet,
            'Predicted-Sentiment': sentiment,
            'Probability-Positive': positive_probability,
            'Probability-Negative': negative_probability,
            'Keywords for Analysis': keywords
        }
    ]
    json_obj = jsonify({'SVM Classification': svm_classification})
    return json_obj

@app.route(version + '/nvb', methods=['GET'])
def naive_bayes_predict():
    tweet = request.args.get('word')
    sentiment, keywords = run().getResult(tweet)
    nvb_classification = [
        { 'Actual-Tweet': tweet,
          'Predicted-Sentiment': sentiment,
          'Keywords for Analysis': keywords
        }
    ]
    return jsonify({'Naive-Bayes Classification': nvb_classification})

if __name__ == '__main__':
    app.run(debug=True)


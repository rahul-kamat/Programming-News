from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/reddit_programming")

#method to get headlines from reddit
def get_headlines():
    user_pass_dict = {'user': 'USERNAME', 'passwd': 'PASSWORD','api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'I am testing Alexa: Rahul'})
    sess.post('https://reddit.com/api/login', data = user_pass_dict)
    time.sleep(1)
    url = 'https://www.reddit.com/r/programming/.json?limit=10'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = []
    for listing in data['data']['children']:
        titles.append(unidecode.unidecode(listing['data']['title']))

    titles = '... '.join([i for i in titles])
    return titles


titles = get_headlines()
print(titles)


#www.website.com/
@app.route('/')
def homepage() :
    return "This app allows Alexa to read programming headlines!"

@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like to hear the latest programming news?'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'The current programming headlines are {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'Ok...bye'
    return statement(bye_text)


if __name__ == '__main__':
    app.run(debug=True)





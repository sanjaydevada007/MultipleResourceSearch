#Resource Search App
from flask import Flask, render_template, request, jsonify
import requests
import cgi
import json
import oauth2 as oauth


app=Flask(__name__)



@app.route('/result',methods=['POST'])
def result():
	a = request.form['find']

	c1="Ly6i7bNwq6ljkWxbJtBirvD6N"
	c2="fWgDUwSxvROriyI1bmRgIYW3h4WAUUvZB4HLePj0CKIdEMbeK1"
	at1="232257533-Zawf3fukYxEfH0i9SQj3ZgfWZWPQtJqNTssEikqm"
	ats="9iFyQ3nhOkWczVq1e6oZJceTobmrYxCOZJnfuhm9WFbBl"

	consumer= oauth.Consumer(key=c1,secret=c2)
	access_token= oauth.Token(key=at1,secret=ats)
	client=oauth.Client(consumer,access_token)
	response, data=client.request('https://api.twitter.com/1.1/search/tweets.json?q='+a+'&result_type=recent')
	tweets=json.loads(data)	
	
	m=requests.get('https://www.googleapis.com/customsearch/v1?key=AIzaSyB__0Nx4NSiwLmttvrqLcq6NfdqcaLoBSU&cx=017576662512468239146:omuauf_lfve&q='+a+'')
	n=requests.get('http://api.duckduckgo.com/?q='+a+'&format=json&pretty=1')
	
	json_object=m.json()
	json_object1=n.json()


	if json_object['queries']['request'][0]['totalResults']!='0':
		lnk=json_object['items'][1]['link']
		txt=json_object['items'][1]['snippet']
	else:
		lnk= "Invalid Search"
		txt="Invalid Search"


	if json_object1['AbstractSource']!="":
		lnk1=json_object1['RelatedTopics'][0]['FirstURL']
		txt1=json_object1['RelatedTopics'][0]['Text']
	else:
		lnk1="Invalid Search"
		txt1="Invalid Search"


	if tweets['statuses']:
		lnk2=tweets['statuses'][0]['source']
		f=len(lnk2)
		txt2=tweets['statuses'][0]['text']
	else:
		lnk2="          None of the recent tweets are found      "
		f=len(lnk2)
		txt2="          None of the recent tweets are found       "

	
	
	x={'query':a,'results':
	{'Google':{'url':lnk,'text':txt},
	'DuckDuckGo':{'url':lnk1,'text':txt1},
	'Twitter':{'url':lnk2[9:f-4],'text':txt2}}}

	return jsonify(x)
	

@app.route('/')
def index():	
	return render_template('index.html')


if __name__ == '__main__':
	app.run()
	
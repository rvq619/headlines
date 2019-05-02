import feedparser 
import json
import urllib2
import urllib


from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=9691311435830b9763122cda33390056'

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
				'cnn': 'http://rss.cnn.com/rss/edition.rss',
				'fox': 'http://feeds.foxnews.com/foxnews/latest',
				'iol': 'http://rss.iol.io/iol/news',
				'guardian': 'https://feeds.theguardian.com/theguardian/world/rss'}

DEFAULTS = {'publication':'bbc',
				'city': 'London, UK'}

@app.route("/")
def home():
	# get customized headlines, based on user input or default
	publication = request.args.get('publication')
	if not publication:
		publication = DEFAULTS['publication']
	articles = get_news(publication)
	# get customized weather based on user input or default
	city = request.args.get('city')
	if not city:
		city = DEFAULTS['city']
	weather = get_weather(city)
	return render_template("home.html", articles=articles, weather=weather)

def get_news(query):
	if not query or query.lower() not in RSS_FEEDS:
		publication = DEFAULTS["publication"]
	else:
		publication = query.lower()
	feed = feedparser.parse(RSS_FEEDS[publication])
	return feed['entries']
	
def get_weather(query):
	query = urllib.quote(query)
	url = WEATHER_URL.format(query)
	data = urllib2.urlopen(url).read()
	parsed = json.loads(data)
	weather = None
	if parsed.get('weather'):
		weather = {'description':parsed['weather'][0]['description'], 'temperature':parsed['main']['temp'], 'city':parsed['name'], 'country':parsed['sys']['country']}
	return weather

if __name__ == '__main__':
    app.run(port=5000, debug=True)
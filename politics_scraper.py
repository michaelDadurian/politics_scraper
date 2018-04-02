from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from time import sleep
#import dbm

search_map = {}
#db = dbm.open('cache', 'c')

search_map['thedailybeast'] = 'Daily Beast'
search_map['rollingstone'] = 'rollingstone.com'
search_map['newsweek'] = 'newsweek'
search_map['nytimes'] = 'new york times'
search_map['bloomberg'] = 'bloomberg'
search_map['huffingtonpost'] = 'huff'
search_map['thinkprogress'] = 'thinkprogress'
search_map['economist'] = 'economist'
search_map['thehill'] = 'the hill'
search_map['washingtonpost'] = 'washington post'
search_map['politico'] = 'politico'
search_map['cnn'] = 'cnn'
search_map['propublica'] = 'propublica'
search_map['msnbc'] = 'msnbc'

def simple_get(url):
	try:
		with closing(get(url, headers = {'User-agent': 'pol scraper'}, stream=True)) as response:
			if is_good_response(response):
				return response.content
			else:
				return None
	except RequestException as e:
		print("error during request")
		
def is_good_response(response):
	content_type = response.headers['Content-Type'].lower()
	print("status code:" , response.status_code)
	return (response.status_code == 200 and content_type is not None and content_type.find('html') > -1)
	

def get_data():
	url = 'https://www.reddit.com/r/politics/'
	response = simple_get(url)
	data = []
	if response is not None:
		html = BeautifulSoup(response, 'html.parser')
		
		div = html.body.find('div', class_ = lambda class_: class_ and class_ == 'content')
		div = div.find('div', id= lambda id: id and id == 'siteTable')
		
		count = 1
		
		for iterator in div:
		
			div_thing = div.contents[count]
			attributes = div_thing.attrs
			if not div_thing == '' and div_thing.name == 'div' and 'thing' in div_thing['class']:
				div_entry = div_thing.find('div', class_ = lambda class_: class_ and 'entry' in class_)
				
				link = div_entry.find('a')['href']
				title = div_entry.find('a').text
				rank = attributes['data-rank']
				
				get_source(link)
				print_data(link, title, rank)
				
				data.append((title,link,rank))
				
				
			count = count + 1
			sleep(3)

		"""
		for each_class in html.select('div[class*="thing id-"]'):
			print (each_class.get_text())
		"""
		
		return data
		
def get_bias(source):
	base_url = 'https://www.allsides.com/media-bias/media-bias-ratings?field_news_source_type_tid=All&field_news_bias_nid=1&title='
	url = base_url + search_map[source]
	
	response = simple_get(url)
	if response is not None:
		html = BeautifulSoup(response, 'html.parser')
		div = html.body.find('div', class_ = lambda class_: class_ and class_ == 'column')
		view_content_div = div.contents[2].find('div', class_ = lambda class_ : class_ and class_ == 'view-content')
		print(view_content_div)
		
	else:
		print('no response')
	
	
def get_source(link):
	tokens = link.split('.')
	site_name = tokens[1]
	get_bias(site_name)
	
def print_data(link, title, rank):
	print("-------------------------------------------------------")
	print("{}: {}".format(rank, title))
	print("link:", link)


get_data()
db.close()
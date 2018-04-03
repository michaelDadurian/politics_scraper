from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from time import sleep
#import dbm

search_map = {}
weight = {}
#db = dbm.open('cache', 'c')

search_map['thedailybeast'] = 'Left'
search_map['rollingstone'] = 'Left'
search_map['newsweek'] = 'Lean Left'
search_map['nytimes'] = 'Lean Left'
search_map['bloomberg'] = 'Center'
search_map['huffingtonpost'] = 'Left'
search_map['thinkprogress'] = 'Left'
search_map['economist'] = 'Lean Left'
search_map['thehill'] = 'Left'
search_map['washingtonpost'] = 'Lean Left'
search_map['politico'] = 'Lean Left'
search_map['cnn'] = 'Left'
search_map['propublica'] = 'Center'
search_map['msnbc'] = 'Left'
search_map['wsj'] = 'Center'
search_map['businessinsider'] = 'Center'
search_map['theatlantic'] = 'Lean Left'
search_map['apnews'] = 'Center'
search_map['rawstory'] = 'Left'
search_map['npr'] = 'Lean Left'
search_map['politifact'] = 'Lean Left'
search_map['washingtonexaminer'] = 'Right'
search_map['buzzfeed'] = 'Left'
search_map['pbs'] = 'Center'
search_map['washingtontimes'] = 'Lean Right'
search_map['cbsnews'] = 'Lean Left'
search_map['abcnews'] = 'Lean Left'
search_map['theintercept'] = 'Left'





def simple_get(url):
	try:
		with closing(get(url, headers = {'User-agent': 'pol scraper'}, stream=True)) as response:
			if is_good_response(response):
				return response.content
			else:
				return None
	except RequestException as e:
		print("error during request")
		
def assign_weight():
	total_points = 0
	for k in search_map:
		if search_map[k] == "Left":
			total_points += -5
		elif search_map[k] == "Right":
			total_points += 5
		elif search_map[k] == "Lean Left":
			total_points -= 3
		elif search_map[k] == "Lean Right":
			total_points += 3
		elif search_map[k] == "Center" or search_map[k] == "No bias found":
			total_points += 0
			
	print("Points:", total_points)
			
			
	
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
				
				website = get_source(link)
				print_data(website, title, rank)
				
				data.append((title,link,rank))
				
				#if rank == 25:
					#break
			
			count = count + 1
			if count == 51:
				break
			
			
			sleep(1)

		"""
		for each_class in html.select('div[class*="thing id-"]'):
			print (each_class.get_text())
		"""
		
		return data

"""		
def get_bias(source):
	base_url = 'https://www.allsides.com/media-bias/media-bias-ratings?field_news_source_type_tid=All&field_news_bias_nid=1&title='
	url = base_url + search_map[source]
	
	response = simple_get(url)
	if response is not None:
		html = BeautifulSoup(response, 'html.parser')
		div = html.body.find('div', class_ = lambda class_: class_ and class_ == 'column')
		
		view_div = div.find('div', class_ = lambda class_: class_ and 'view-allsides-daily' in class_)
		print(div.contents)
		print("----------------------------------------------------------")
		print(view_div.contents)
		
		
		#div_entry = view_div.find('div', class_ = lambda class_: class_ and class_ == 'view-content')
		#print(div_entry)
		
	else:
		print('no response')
"""	
	
def get_source(link):
	tokens = link.split('.')
	#print(tokens)
	if 'com' in tokens[1] or 'go' in tokens[1]:
		site_name = tokens[0].split('/')
		site_name = site_name[2]
		#print(site_name)
	else:
		site_name = tokens[1]
	return site_name
	#get_bias(site_name)
	
def print_data(website, title, rank):
	print("-----------------------------------------------------------------------------------------------------")
	print("{}: {}".format(rank, title))
	print("source: {}".format(website.upper()))
	if website in search_map.keys():
		print("bias: {}".format(search_map[website]))
	else:
		print("No bias found.")
		search_map[website] = "No bias found"
		


get_data()
print("---------------------------------------------------------------------------------------------")
assign_weight()
#db.close()
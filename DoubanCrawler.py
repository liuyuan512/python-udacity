import requests
from bs4 import BeautifulSoup
# import expanddouban


def getMovieUrl(category, location):
	url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags={},{}".format(category,location)
	return url





class Movie(object):
	def __init__(self,name,rate,location,category,info_link,cover_link):
		self.name = name
		self.rate = rate
		self.location = location
		self.category = category
		self.info_link = info_link
		self.cover_link = cover_link



"""
return a list of Movie objects with the given category and location.
"""
def getMovies(category, location):
	url = getMovieUrl(category, location)
	response = requests.get(url)
	html = response.text
	soup = BeautifulSoup(html,'html.parser')
	content = soup.find(id="content").find_all("a",class_="item")
	print(soup)

# getMovies("%e7%94%b5%e5%bd%b1","%e7%be%8e%e5%9b%bd")
getMovies("电影","美国")

# htmll = expanddouban.getHtml("https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影，美国")
# print(htmll)
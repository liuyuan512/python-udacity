import csv
from bs4 import BeautifulSoup
import expanddouban
import codecs

movie_list = []
location_list = ["美国","英国","香港","大陆","台湾","日本","韩国","法国","德国","意大利","西班牙","印度","泰国","俄罗斯","伊朗","加拿大","澳大利亚","爱尔兰","瑞典","巴西","丹麦"]
category_list = ["爱情","喜剧","科幻"]



def getMovieUrl(category, location):
	url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}".format(category,location)
	return url


class Movie(object):
	def __init__(self,name,rate,location,category,info_link,cover_link):
		self.name = name
		self.rate = rate
		self.location = location
		self.category = category
		self.info_link = info_link
		self.cover_link = cover_link


def getMovies(category, location):
	url = getMovieUrl(category, location)
	html = expanddouban.getHtml(url)
	soup = BeautifulSoup(html,'html.parser')
	content = soup.find(id="content").find(class_="list-wp").find_all("a",class_="item")
	for element in content:
		cover_link = element.find("img").get("src")
		name = element.find("p").find(class_="title").string
		rate = element.find("p").find(class_="rate").string
		info_link = element.get("href")
		m =  Movie(name,rate,location,category,info_link,cover_link)
		movie_list.append(m)

def getMovieCSV():
	for c in category_list:
		for l in location_list:
			getMovies(c,l)
	with codecs.open('movies.csv', 'w', 'utf_8_sig') as csv_file:
		 csv_app = csv.writer(csv_file)
		 for m in movie_list:
			 m_l = [m.name,m.rate,m.location,m.category,m.info_link,m.cover_link]
			 csv_app.writerow(m_l)

def sort_by_value(d):
	return sorted(d.items(), key=lambda d: d[1])


def getMovieDict(movie_category):
	dict = {}
	for l in location_list:
		movie_l = []
		for m in movie_category:
			if m[2] == l:
				movie_l.append(m)
				dict[l] = round(len(movie_l) / len(movie_category) * 100, 2)
	return dict
def getMovieData():
	getMovieCSV()
	with open('movies.csv', 'r') as f:
		csv_app = csv.reader(f)
		movies = list(csv_app)
		movie_love = []
		movie_comedy = []
		movie_fiction = []
		for m in movies:
			if m[3] == category_list[0]:
				movie_love.append(m)
			elif m[3] == category_list[1]:
				movie_comedy.append(m)
			else:
				movie_fiction.append(m)
		dict_love = sort_by_value(getMovieDict(movie_love))
		dict_comedy = sort_by_value(getMovieDict(movie_comedy))
		dict_fiction = sort_by_value(getMovieDict(movie_fiction))
	with open("output.txt", "w") as txt_file:
		txt_file.write("爱情电影中，排名前三的地区是{}、{}、{},占此类别电影总数的百分比分别为:{}%,{}%,{}%\n".format(dict_love[-1][0],dict_love[-2][0],dict_love[-3][0],dict_love[-1][1],dict_love[-2][1],dict_love[-3][1]))
		txt_file.write("喜剧电影中，排名前三的地区是{}、{}、{},占此类别电影总数的百分比分别为:{}%,{}%,{}%\n".format(dict_comedy[-1][0],dict_comedy[-2][0],dict_comedy[-3][0],dict_comedy[-1][1],dict_comedy[-2][1],dict_comedy[-3][1]))
		txt_file.write("科幻电影中，排名前三的地区是{}、{}、{},占此类别电影总数的百分比分别为:{}%,{}%,{}%\n".format(dict_fiction[-1][0],dict_fiction[-2][0],dict_fiction[-3][0],dict_fiction[-1][1],dict_fiction[-2][1],dict_fiction[-3][1]))
getMovieData()


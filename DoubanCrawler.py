import csv
from bs4 import BeautifulSoup
import expanddouban


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


"""
return a list of Movie objects with the given category and location.
	m = Movie(element.title,element.rate)

"""
movie_list = []


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
	# print(movie_list)
	# print(content)

def getMovieCSV():

	getMovies("美国","剧情")
	getMovies("香港","动作")
	getMovies("英国","剧情")
	with open("movies.csv","a") as csv_file:
		csv_app = csv.writer(csv_file)
		for m in movie_list:
			m_l = [m.name,m.rate,m.location,m.category,m.info_link,m.cover_link]
			csv_app.writerow(m_l)

def getMovieData():
	getMovieCSV()
	with open('movies.csv', 'r') as f:
		csv_app = csv.reader(f)
		movies = list(csv_app)
		movie_story = []
		movie_action = []
		movie_story_a = []
		movie_story_e = []
		for m in movies:
			if m[2] == "剧情":
				movie_story.append(m)
			else:
				movie_action.append(m)
		if len(movie_story) != 0:
			for m in movie_story:
				if m[3] == "美国":
					movie_story_a.append(m)
				else:
					movie_story_e.append(m)
		print("movie_story=====",len(movie_story),"movie_action======",len(movie_action),len(movie_story_a),len(movie_story_e))
		# print(movies)
	with open("output.txt", "a") as txt_file:
		txt_file.write("种类为剧情的电影一共有{}个\n".format(len(movie_story)))
		txt_file.write("在种类为剧情的电影里面，地区为美国的有{}个，占此类电影的百分比为{}，地区为英国的有{}个，占此类电影的百分比为{}\n".format(len(movie_story_a),len(movie_story_a)/len(movie_story),len(movie_story_e),len(movie_story_e)/len(movie_story),))
		txt_file.write("种类为动作，地区为香港的电影一共有{}个\n".format(len(movie_action)))
getMovieData()


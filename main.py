from bs4 import BeautifulSoup
import requests
import pandas as pd
url = "https://www.imdb.com/chart/top/"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")


def get_movie_links(doc):
    urls = []
    links = doc.find_all("td", class_="titleColumn")
    for i in links:
        f = i.find_all("a")
        for a in f:
            urls.append(a.get("href"))

    base_url = "https://imdb.com"
    movies_links = [base_url + link for link in urls]
    return movies_links


list_movies_links = get_movie_links(doc)

print(list_movies_links)


def get_movie_names(doc):
    movie_names = []
    names = doc.find_all("td", class_="titleColumn")
    for name in names:
        f = name.find_all("a")
        for a in f:
            movie_names.append(a.text)
    return movie_names


list_movie_names = get_movie_names(doc)
print(list_movie_names)


def get_movie_production_year(doc):
    list_movie_production_year = []
    years = doc.find_all("td", class_="titleColumn")
    for year in years:
        g = year.find_all("span")
        for b in g:
            list_movie_production_year.append(int(b.text[1:-1]))

    return list_movie_production_year


list_year_production = get_movie_production_year(doc)
print(list_year_production)


def get_rating_stars(doc):
    rating_stars = []
    stars = doc.find_all("td", class_="ratingColumn imdbRating")
    for z in stars:
        h = z.find_all("strong")
        for k in z:
            rating_stars.append(k.text)
    rating_stars_filtered = [star for star in rating_stars if star != "\n"]
    return rating_stars_filtered


list_rating_stars = get_rating_stars(doc)
print(list_rating_stars)
def create_rank():
    rank=[]
    for i in range(250):
        rank.append(i+1)
    return rank

ranks=create_rank()
print(ranks)

url_movie=list_movies_links[1]
print(url_movie)

def scrape_imdb_250(doc):
    url = "https://www.imdb.com/chart/top/"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    top_movies_dict={
        "rank":create_rank(),
        "Title":get_movie_names(doc),
        "Movie Launched":get_movie_production_year(doc),
        "Rating":get_rating_stars(doc)}
    return top_movies_dict
Top_250_IMDB = pd.DataFrame(scrape_imdb_250(doc))
Top_250_IMDB.to_csv("Top_Movies_250_IMDB", index=None)
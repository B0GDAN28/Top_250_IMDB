from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

movie_url = "https://www.imdb.com/chart/top/"


def get_top_250(movie_url_):
    result = requests.get(movie_url_)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br",

        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"
    }
    movie_doc2 = requests.get(movie_url_, headers=headers)
    movie_doc_top250 = BeautifulSoup(movie_doc2.text, 'html.parser')
    return movie_doc_top250


doc = get_top_250(movie_url)


def get_movie_links(doc_):
    urls = []
    links = doc_.find_all("td", class_="titleColumn")

    for a in links:
        f = a.find_all("a")
        for href in f:
            urls.append(href.get("href"))

    base_url = "https://imdb.com"
    movies_links = [base_url + link for link in urls]
    return movies_links


list_movies_links = get_movie_links(doc)


def get_movie_names(doc_):
    movie_names = []
    names = doc_.find_all("td", class_="titleColumn")
    for name_link in names:
        f = name_link.find_all("a")
        for name in f:
            movie_names.append(name.text)
    return movie_names


list_movie_names = get_movie_names(doc)


def get_movie_production_year(doc_):
    list_movie_production_year = []
    years = doc_.find_all("td", class_="titleColumn")
    for year_span in years:
        spans = year_span.find_all("span")
        for movie_year in spans:
            list_movie_production_year.append((movie_year.text[1:-1]))

    return list_movie_production_year


list_year_production = get_movie_production_year(doc)


def get_rating_stars(doc_):
    rating_stars = []
    stars = doc_.find_all("td", class_="ratingColumn imdbRating")

    for rating in stars:
        rating_strong = rating.find_all("strong")
        for star_rating in rating_strong:
            rating_stars.append(star_rating.text)
    rating_stars_filtered = [star for star in rating_stars if star != "\n"]
    return rating_stars_filtered


list_rating_stars = get_rating_stars(doc)


def create_rank():
    ranks = []
    for rank in range(250):
        ranks.append(rank + 1)
    return ranks


ranks = create_rank()


def scrape_imdb_250(doc_):
    # url = "https://www.imdb.com/chart/top/"
    # result = requests.get(url)
    # doc = BeautifulSoup(result.text, "html.parser")
    top_movies_dict = {
        "rank": create_rank(),
        "Title": get_movie_names(doc_),
        "Movie Launched": get_movie_production_year(doc_),
        "Rating": get_rating_stars(doc_)}
    return top_movies_dict


Top_250_IMDB = pd.DataFrame(scrape_imdb_250(doc))
Top_250_IMDB.to_csv("Top_Movies_250_IMDB", index=None)
# URL of the webscraping movie
movie_link = get_movie_links(doc)


def get_movie_url(movie_link_):
    movie_doc1 = requests.get(movie_link_)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "Upgrade-Insecure-Requests": "1"
    }
    movie_doc2 = requests.get(movie_link_, headers=headers)
    movie_doc = BeautifulSoup(movie_doc2.text, 'html.parser')
    return movie_doc


movie_doc = get_movie_url(movie_link[0])


def get_movie_type(movie_doc_):
    movie_types = []
    try:
        types = movie_doc_.find_all("div", class_="ipc-chip-list__scroller")
        for types in types:
            g = types.find_all("a")
            for b in g:
                movie_types.append(b.text)
        return movie_types
    except (AttributeError, ValueError, IndexError):
        movie_types = ['Not Found']
        return movie_types


list_movie_types = get_movie_type(movie_doc)


def get_number_user_rating(movie_doc_):
    list_number_user_rating = []
    try:
        numbers = movie_doc_.find_all("div", class_="sc-bde20123-3 bjjENQ")
        for number in numbers:
            list_number_user_rating.append(number.text)
        return list_number_user_rating
    except (AttributeError, ValueError, IndexError):
        number = "Not found"
        return number


number_user_rating = get_number_user_rating(movie_doc)


def get_directors(movie_doc_):
    try:
        directors = movie_doc_.find("div", class_="ipc-metadata-list-item__content-container")
        directors1 = [director.text for director in directors]
        return directors1
    except (TypeError, ValueError, IndexError):
        directors1 = ['Not found']
        return directors1


list_directors = get_directors(movie_doc)


def get_writers(movie_doc_):
    try:
        writers = movie_doc_.find("li", class_="ipc-metadata-list__item ipc-metadata-list-item--link")
        children = writers.findChildren("div", class_="ipc-metadata-list-item__content-container")
        writers1 = [writer.text for writer in children]
        return writers1
    except TypeError:
        writers1 = ['Not found']
        return writers1


list_writers = get_writers(movie_doc)
for i in range(len(list_writers)):
    spaced_name = ''
    for j in range(len(list_writers[i])):
        if j > 0 and list_writers[i][j].isupper():
            spaced_name += ' ' + list_writers[i][j]
        else:
            spaced_name += list_writers[i][j]
    list_writers[i] = spaced_name

top_movie_details_dict = {
    "Rank": create_rank(),
    "Movie Name": get_movie_names(doc),
    "Production Year": get_movie_production_year(doc),
    "Rating": get_rating_stars(doc),
    "Genre": [],
    "Number of user ratings": [],
    "Director/Directors": [],
    "Writer/Writers": [],
    "Link": get_movie_links(doc)
}
try:
    for i in range(len(movie_link)):
        top_movie_details_dict["Genre"].append(get_movie_type(movie_link[i]))
        top_movie_details_dict["Number of user ratings"].append(get_number_user_rating(movie_link[i]))
        top_movie_details_dict["Director/Directors"].append(get_directors(movie_link[i]))
        top_movie_details_dict["Writer/Writers"].append(get_writers(movie_link[i]))

except ValueError:
    print("DONT WORK")

description = pd.DataFrame(top_movie_details_dict)

description.to_csv("Top_250_IMDB_MOVIES", index=False)

df = pd.DataFrame(top_movie_details_dict)


def get_list_of_unique_elements(df_, column):
    list_of_unique = []
    for element in column:
        if element not in list_of_unique:
            list_of_unique.append(element)
    return list_of_unique


list_of_unique_ratings = get_list_of_unique_elements(df, get_rating_stars(doc))


def get_list_of_all_elements(df_, column):
    list_of_all = []
    for element in column:
        list_of_all.append(element)
    return list_of_all


list_of_all_ratings = get_list_of_all_elements(df, get_rating_stars(doc))


def get_appearances_count(list_of_all_, list_of_unique_):
    appearances_count = []
    for unique in list_of_unique_:
        count = 0
        for element in list_of_all_:
            if unique == element:
                count = count + 1
        appearances_count.append(count)
    return appearances_count


x = np.array(get_list_of_unique_elements(df, get_rating_stars(doc)))
y = np.array(get_appearances_count(list_of_all_ratings, list_of_unique_ratings))
plt.plot(x, y)

plt.title("Movie Ratings")
plt.xlabel("Rating Number")
plt.ylabel("Number of Movies")
plt.show()
list_of_all_years_movies = get_list_of_all_elements(df, get_movie_production_year(doc))
list_of_unique_year_movies = get_list_of_unique_elements(df, get_movie_production_year(doc))
movie_appearances = get_appearances_count(list_of_all_years_movies, list_of_unique_year_movies)


def get_decade(list_of_unique_year_movies_):
    list_unique_years_rounded = []
    for year in list_of_unique_year_movies_:
        list_unique_years_rounded.append(year[:-1])
    list_year_decades = []
    for rounded in list_unique_years_rounded:
        list_year_decades.append(rounded + 'Os')
    return list_year_decades


list_movies_decades = get_decade(list_of_unique_year_movies)


def get_unique_decades(list_movie_decades):
    list_of_unique_decades = []
    for decade in list_movie_decades:
        if decade not in list_of_unique_decades:
            list_of_unique_decades.append(decade)
    return list_of_unique_decades


def get_appearances_count_decade(list_movies_decades_, list_unique_decades_):
    appearances_count = []
    for unique_decade in list_unique_decades_:
        count = 0
        for element in list_movies_decades_:
            if unique_decade == element:
                count = count + 1
        appearances_count.append(count)
    return appearances_count


list_unique_decades = get_unique_decades(list_movies_decades)
list_decades_appearances = get_appearances_count_decade(list_movies_decades, list_unique_decades)

x = np.array(get_appearances_count_decade(list_movies_decades, list_unique_decades))
y = np.array(list_unique_decades)
plt.plot(x, y)

plt.title("Movie decades")
plt.xlabel("Number of Movies")
plt.ylabel("Decades")
plt.show()

if __name__ == '__main__':
    print(list_movies_links)
    print(list_movie_names)
    # print(movie_doc)
    print(len(list_movie_names))
    print(len(list_movies_links))
    print(list_year_production)
    print(len(list_year_production))
    print(list_rating_stars)
    print(len(list_rating_stars))
    print(ranks)
    print(len(ranks))
    # print(movie_url)
    print(number_user_rating)
    print(list_directors)
    print(list_writers)
    print(len(list_movies_links), len(list_movie_names), len(list_year_production), len(list_rating_stars), len(ranks),
          len(list_movie_types),
          len(number_user_rating), len(list_directors), len(list_writers))
    print(top_movie_details_dict)
    print(len(list_of_all_years_movies))
    print(list_of_unique_year_movies)
    print(movie_appearances)
    print(len(list_movies_decades))
    print(len(list_unique_decades))
    print(list_decades_appearances)

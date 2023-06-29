from bs4 import BeautifulSoup
import requests
import pandas as pd

movie_url = "https://www.imdb.com/chart/top/"


def get_top_250(movie_url):
    result = requests.get(movie_url)
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
    movie_doc2 = requests.get(movie_url, headers=headers)
    movie_doc = BeautifulSoup(movie_doc2.text, 'html.parser')
    return movie_doc


doc = get_top_250(movie_url)


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

# print(list_movies_links)
print(len(list_movies_links))


def get_movie_names(doc):
    movie_names = []
    names = doc.find_all("td", class_="titleColumn")
    for name in names:
        f = name.find_all("a")
        for a in f:
            movie_names.append(a.text)
    return movie_names


list_movie_names = get_movie_names(doc)
# print(list_movie_names)
print(len(list_movie_names))


def get_movie_production_year(doc):
    list_movie_production_year = []
    years = doc.find_all("td", class_="titleColumn")
    for year in years:
        g = year.find_all("span")
        for b in g:
            list_movie_production_year.append(int(b.text[1:-1]))

    return list_movie_production_year


list_year_production = get_movie_production_year(doc)
# print(list_year_production)
print(len(list_year_production))


def get_rating_stars(doc):
    rating_stars = []
    stars = doc.find_all("td", class_="ratingColumn imdbRating")

    for z in stars:
        h = z.find_all("strong")
        for k in h:
            rating_stars.append(k.text)
    rating_stars_filtered = [star for star in rating_stars if star != "\n"]
    return rating_stars_filtered


list_rating_stars = get_rating_stars(doc)
# print(list_rating_stars)
print(len(list_rating_stars))


def create_rank():
    rank = []
    for i in range(250):
        rank.append(i + 1)
    return rank


ranks = create_rank()
# print(ranks)
print(len(ranks))


def scrape_imdb_250(doc):
    # url = "https://www.imdb.com/chart/top/"
    # result = requests.get(url)
    # doc = BeautifulSoup(result.text, "html.parser")
    top_movies_dict = {
        "rank": create_rank(),
        "Title": get_movie_names(doc),
        "Movie Launched": get_movie_production_year(doc),
        "Rating": get_rating_stars(doc)}
    return top_movies_dict


Top_250_IMDB = pd.DataFrame(scrape_imdb_250(doc))
Top_250_IMDB.to_csv("Top_Movies_250_IMDB", index=None)
# URL of the webscraping movie
movie_link = get_movie_links(doc)


# print(movie_url)


def get_movie_url(movie_link):
    movie_doc1 = requests.get(movie_link)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "Upgrade-Insecure-Requests": "1"
    }
    movie_doc2 = requests.get(movie_link, headers=headers)
    movie_doc = BeautifulSoup(movie_doc2.text, 'html.parser')
    return movie_doc


movie_doc = get_movie_url(movie_link[0])


# print(movie_doc)


def get_movie_type(movie_doc):
    movie_types = []
    try:
        types = movie_doc.find_all("div", class_="ipc-chip-list__scroller")
        for types in types:
            g = types.find_all("a")
            for b in g:
                movie_types.append(b.text)
        return movie_types
    except (AttributeError, ValueError, IndexError):
        movie_types = ['Not Found']
        return movie_types


list_movie_types = get_movie_type(movie_doc)


print(list_movie_types)


def get_number_user_rating(movie_doc):
    list_number_user_rating = []
    try:
        numbers = movie_doc.find_all("div", class_="sc-bde20123-3 bjjENQ")
        for number in numbers:
            list_number_user_rating.append(number.text)
        return list_number_user_rating
    except (AttributeError, ValueError, IndexError):
        number = "Not found"
        return number


number_user_rating = get_number_user_rating(movie_doc)
print(number_user_rating)


def get_directors(movie_doc):
    try:
        directors = movie_doc.find("div", class_="ipc-metadata-list-item__content-container")
        directors1 = [director.text for director in directors]
        return directors1
    except (TypeError, ValueError, IndexError):
        directors1 = ['Not found']
        return directors1


list_directors = get_directors(movie_doc)
print(list_directors)


def get_writers(movie_doc):
    try:
        writers = movie_doc.find("li", class_="ipc-metadata-list__item ipc-metadata-list-item--link")
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
print(list_writers)
print(len(list_movies_links), len(list_movie_names), len(list_year_production), len(list_rating_stars), len(ranks),
      len(list_movie_types),
      len(number_user_rating), len(list_directors), len(list_writers))


top_movie_details_dict = {
    "Rank": create_rank(),
    "Movie Name": get_movie_names(doc),
    "Production Year": get_movie_production_year(doc),
    "Rating": get_rating_stars(doc),
    "Genre": [],
    "Number of user ratings": [],
    "Director/Directos": [],
    "Writer/Writers": [],
    "Link": get_movie_links(doc)
}
try:
    for i in range(len(movie_link)):
        top_movie_details_dict["Genre"].append(get_movie_type(movie_link[i]))
        top_movie_details_dict["Number of user ratings"].append(get_number_user_rating(movie_link[i]))
        top_movie_details_dict["Director/Directos"].append(get_directors(movie_link[i]))
        top_movie_details_dict["Writer/Writers"].append(get_writers(movie_link[i]))

except ValueError:
    print("DONT WORK")
print(top_movie_details_dict)
key_lengths = {key: len(key) for key in top_movie_details_dict.keys()}

# Print the lengths of each key
for key, length in key_lengths.items():
    print(f"Length of key '{key}': {length}")
array_lengths = set(len(array) for array in top_movie_details_dict.values())
if len(array_lengths) == 1:
    print("All arrays have the same length.")
else:
    print("Arrays have different lengths:", array_lengths)

description = pd.DataFrame(top_movie_details_dict)

description.to_csv("Top_250_IMDB_MOVIES", index=False)

from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from tmdbv3api import TMDb
from tmdbv3api import Movie
from tmdbv3api import Discover
import datetime
from datetime import timedelta, timezone
tmdb = TMDb()
# tmdb.api_key = 'PRIVATE_KEY'
tmdb.language = 'en'
tmdb.debug = True

movie = Movie()
popular = movie.popular()

def create_list_of_titles_from_api():
    date = datetime.datetime.now()

    date_minus_5_years = date - timedelta(days=7300)

    output_file = open("output_titles.txt", "w")
    discover = Discover()
    movie_details = Movie()
    list = []

    for _ in range(6000):
        date_plus_5_days = date_minus_5_years + timedelta(days=3)
        movie = discover.discover_movies({
            'primary_release_date.gte': str(date_minus_5_years).split(" ")[0],
            'primary_release_date.lte': str(date_plus_5_days).split(" ")[0]
        })

        date_minus_5_years = date_minus_5_years + timedelta(days=3)

        for movies in movie:
            m = movie_details.details((movie[0]["id"]))
            if str(movie[0]["title"]) not in list:
                list.append(str(movie[0]["title"]))
                output_file.write(str(movie[0]["title"]))
                output_file.write("\n")
    return scrape_titles_from_rotten(output_file)


def create_list(file_name):
    output = open("editedFile.txt","w")
    for lines in open(file_name,"r"):
        lines = lines.replace(" ", "_")
        lines = lines.replace(":", "")
        output.write(lines)


def print_data(file_name):
    for lines in open(file_name,"r"):
        print(lines)

def fix_dataset(file_name):
    output = open("TrainingMovieDataset.txt", "w")
    for lines in open(file_name, "r"):
        try:
            if type(int(lines.split(",")[0])) == type(6) and len(lines.split(",")[1]) != 1:
                output.write(str(lines))
        except:
            continue
    return output

def scrape_titles_from_rotten(file_name):
    options = Options()
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')
    options.headless = False
    driver = webdriver.Chrome("/Users/gerardo/PycharmProjects/elasticsearch/chromedriver", options=options)
    output_file = open("movieDataset.txt", "w")

    for titles in open(file_name, "r"):
        try:
            driver.get('https://www.rottentomatoes.com/m/' + titles)
            score = driver.find_element_by_tag_name('score-board')

            overview = driver.find_element_by_class_name("movie_synopsis.clamp.clamp-6.js-clamp")

            output_file.write(str(score.get_attribute("audiencescore")) + "," + str(overview.text) )
            output_file.write("\n")

        except Exception as exception:
            print(exception)
            continue
    output = fix_dataset(output_file)
    return output











import requests
from lxml import html
import json
from scraping.model.Movie import Movie
from multiprocessing.dummy import Pool as ThreadPool


url = 'http://ilcorsaronero.info'
latest = 'http://ilcorsaronero.info/recenti'
search = 'http://ilcorsaronero.info/argh.php?search='

xpath_names = '//tr[@class = "odd" or @class = "odd2"]/td[1]/a[text() = "BDRiP" or text() = "DVD" or text() = "SerieTv"]/../../td[2]/a/text()'
xpath_objects = '//tr[@class = "odd" or @class = "odd2"]/td[1]/a[text() = "BDRiP" or text() = "DVD" or text() = "SerieTv"]/../../td[2]/a'
movie_list = []

def add_object_to_queue(url):
    page = get_page(url)
    movie_list.append(Movie(page))

def get_page(url):
    return requests.get(url)

def get_movie(query):
    global movie_list

    movie_list = []
    query_url = "{0}{1}".format(search,query)
    page = get_page(query_url)
    tree = html.fromstring(page.text)
    objects = tree.xpath(xpath_objects)
    pool = ThreadPool(20)
    pool.map(add_object_to_queue, map(lambda obj: obj.attrib['href'], objects[0:10]))
    pool.close()
    pool.join()
    return json.dumps([ob.__dict__ for ob in movie_list])

def get_movie_details(id):
    query_url = "{0}{1}{2}{3}".format(url,'/tor/',id, '/a')
    page = get_page(query_url)
    movie = Movie(page)

    return json.dumps(movie.__dict__)

def get_latest():
    movie_list = []
    page = get_page(latest)
    tree = html.fromstring(page.text)
    objects = tree.xpath(xpath_objects)

    #add_object_to_queue(main_queue,  "{0}{1}".format(url, objects[0].attrib['href']))
    #pool = ThreadPool(len(objects)-1)

    pool = ThreadPool(20)
    res = pool.map(add_object_to_queue, map(lambda obj: "{0}{1}".format(url, obj.attrib['href']), objects[0:10]))
    pool.close()
    pool.join()
    return json.dumps([ob.__dict__ for ob in movie_list])


from lxml import html
import requests

it_root = "https://it.wikipedia.org/wiki/"
xpath_lang = '//a[@hreflang = "en"]'


def get_english_moviename(movie_name):

    #[todo] replace spaces with _
    page = requests.get("{0}{1}".format(it_root, movie_name))
    tree = html.fromstring(page.text)
    elems = tree.xpath(xpath_lang)
    title = ""

    try:
        objects = filter( lambda item: str(item.attrib['href']).__contains__("wikipedia") ,elems)[0]
        new_link = objects.attrib['href']
        page = requests.get(new_link)
        tree = html.fromstring(page.text)
        title = tree.xpath("//title/text()")[0]
        title = title.split(' - ')[0]
    except Exception, e:
        print e.message
        title = ""
    return title
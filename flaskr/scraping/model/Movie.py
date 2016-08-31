class Movie(object):
    def __init__(self, page):
        self.peers = 0
        self.leech = 0
        self.magnet = None
        self.cat = None
        self.title = None
        self.size = None
        self.date_added = None
        self.image = None
        self.descr = None
        self.id = None
        self.load_data(page)

    def load_data(self, page):
        from lxml import html
        tree = html.fromstring(page.content)
        self.id = page.url.split('/')[4]
        self.load_seeds_and_peers(tree)
        self.load_cat(tree)
        self.load_magnet(tree)
        self.load_title(tree)
        self.load_size(tree)
        self.load_date(tree)
        self.load_img(tree)

    def load_seeds_and_peers(self, tree):

        elements = tree.xpath('//tr[@class = "odd" or @class = "odd2"]/td/font/text()')

        if len(elements) < 2:
            raise IndexError("Missing elements")
        self.seeds = elements[0]
        self.leech = elements[1]

    def load_magnet(self, tree):
        self.magnet = tree.xpath('//td[@class = "header2"]/form/a')[0].attrib['href']

    def load_cat(self, tree):
        self.cat = tree.xpath('//tr[@class = "odd2"]/td[text() = "Categoria bittorrent"]/../td[2]/text()')[0]

    def load_title(self, tree):
        self.title = tree.xpath('//center/b/font/text()')[0]

        if self.title is not None:
            self.title = self.title.replace(" - ", "")

    def load_size(self, tree):
        self.size = tree.xpath('//tr/td[text() = "Size"]/../td[2]/text()')[0]

    def load_date(self, tree):
        self.date_added = tree.xpath('//tr/td[text() = "Aggiunto"]/../td[2]/text()')[0].split(' ')[0]

    def load_img(self, tree):
        try:
            self.image =  tree.xpath('//tr/td[text() = "Descrizione"]/../td[2]/div/i/img[1]')[0].attrib['src']
        except:
            print "Failed to load image"
            self.image = None


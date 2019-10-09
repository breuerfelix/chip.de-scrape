from bs4 import BeautifulSoup as Soup
from os import listdir

page = Soup(page, "html.parser")

news = page.find_all("section", class_="Grid__Container Skin--Light")
news = news[0]
newslist = news.find_all("div", class_="ListItem mt-sm")


for new in newslist:
    atag = new.find("a", class_="ListItem__TextLink")

    link = atag["href"]

    title = atag.h2.text
    date = atag.aside.find_all("span")[1].text

    # replace whitespace in title
    title = slugify(title)

    date = date.strip()
    # formate date
    date = date.split(" ")[1]
    date = date.split(".")
    day = date[0]
    month = date[1]
    year = date[2]

    dirname = "{}/{}/{}/{}/".format(database, year, month, day)

    found = False
    if os.path.exists(dirname):
        pass

from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen, Request
import os
from os import listdir
import time
from threading import Thread


def writeFile(path, source):
    with open(path, "w+") as f:
        f.write(source)


def createFolder(dirname):
    if not os.path.exists(os.path.dirname(dirname)):
        os.makedirs(os.path.dirname(dirname))


def slugify(filename, replace=" "):
    import unicodedata
    import string

    filename = filename.replace("ü", "ue")
    filename = filename.replace("ö", "oe")
    filename = filename.replace("ä", "ae")

    whitelist = "-_.() %s%s" % (string.ascii_letters, string.digits)

    # remove whitespace
    filename = filename.strip()

    # replace spaces
    for r in replace:
        filename = filename.replace(r, "_")

    # keep only valid ascii chars
    cleaned_filename = (
        unicodedata.normalize("NFKD", filename).encode("ASCII", "ignore").decode()
    )

    # keep only whitelisted chars
    return "".join(c for c in cleaned_filename if c in whitelist)


def threadFunc():
    while True:
        database = "/var/www/articles/chip.de"

        chip = "https://www.chip.de/nachrichten"

        req = Request(chip)
        req.add_header("Cache-Control", "max-age=0")
        res = urlopen(req)
        page = res.read()
        # fp = urlopen(chip)
        # time.sleep(5)
        # page = fp.read()
        # time.sleep(5)
        # fp.close()
        res.close()

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
                # check if file exists
                files = listdir(dirname)
                for file in files:
                    if title in file:
                        found = True
                        break
            else:
                found = False

            if not found:
                try:
                    createFolder(dirname)

                    # opens article to get page source
                    client = urlopen(link)
                    article = client.read()
                    client.close()

                    articleSoup = Soup(article, "html.parser")
                    metaDate = articleSoup.find("meta", itemprop="datePublished")
                    content = metaDate["content"]

                    timeString = content.split("T")[1]
                    hour = timeString.split(":")[0]
                    minute = timeString.split(":")[1]

                    writeFile(
                        dirname + hour + "-" + minute + "-" + title + ".html",
                        articleSoup.prettify(),
                    )
                    print("article added: " + title)
                except:
                    print("error parsing article: " + title)

        # goto sleep
        time.sleep(120)


threadFunc()

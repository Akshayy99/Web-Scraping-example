import requests
from bs4 import BeautifulSoup
import csv


NAMES = ["Name"]
AUTHORS = ["Author"]
URLs = ["URL"]
NUM_RATINGS = ["Number of ratings"]
RATING = ["Average rating"]
PRICES = ["Price"]
common = "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_"
loop_link = "?ie=UTF8&pg="


for i in range(1, 6):
    url = common + str(i) + loop_link + str(i)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    main = soup.find_all('div', class_='zg_itemImmersion')

    for i in main:
        # finding book names
        nam = i.find(class_='p13n-sc-truncate p13n-sc-line-clamp-1').get_text()
        NAMES.append(nam)

        # finding URLs of books
        par = i.find('div', class_='a-section a-spacing-none p13n-asin')
        if par:
            sublink = par.find('a', class_='a-link-normal').get('href')
            URLs.append("https://www.amazon.in" + sublink)
        else:
            URLs.append("Not available")

        # finding author names
        auth = i.find('div', class_='a-row a-size-small')
        if auth:
            AUTHORS.append(auth.string)
        else:
            AUTHORS.append("Not available")

        # finding prices of books
        out = i.find('a', class_='a-link-normal a-text-normal')
        if out:
            price = out.find('span', class_='p13n-sc-price').getText()
            PRICES.append(price)
        else:
            PRICES.append("Not available")

        # finding number of ratings
        rat_ = i.find("div", class_='a-icon-row a-spacing-none')
        if rat_:
            rating = rat_.find('i')
            NUM_RATINGS.append(rating.string)
        else:
            NUM_RATINGS.append("Not available")

        # finding average ratings
        average = i.find('div', class_='a-icon-row a-spacing-none')
        if average:
            stars = average.find('a', class_='a-size-small a-link-normal')
            RATING.append(stars.string)
        else:
            RATING.append("Not available")


rows = zip(NAMES, URLs, AUTHORS, PRICES, NUM_RATINGS, RATING)

with open('output/in_book.csv', "w") as f:
    writer = csv.writer(f, delimiter=";")
    for row in rows:
        writer.writerow(row)

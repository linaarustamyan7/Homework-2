# -*- coding: utf-8 -*-
"""Homework2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1glX6Vrd2yecK8Hzi-Ik7t_KVCijFBzTm
"""

!pip install response

!pip install scrapy

!pip install pandas

import time
import requests
import response
import numpy as np
import pandas as pd
from scrapy.http import TextResponse

"""#Problem 1"""

url = "http://quotes.toscrape.com/"
base_url = "http://quotes.toscrape.com"

class Quotes:

    def __init__(self,URL):
        self.URL = URL
        self.page = requests.get(self.URL)
        self.response = TextResponse(body=self.page.text,url=self.URL,encoding="utf-8")

    def quote_scraper(self):
        """
        Scraping the quotes, authors, tags and the hyperlinks 
        
        """
        quotes = self.response.css("span.text::text").extract()
        authors = self.response.css("small.author::text").extract() 
        tags = [i.css("a.tag::text").extract() for i in self.response.css("div.tags")]
        hyperlinks = [base_url+i for i in self.response.css("small.author ~ a::attr(href)").extract()]
        return {"Quotes":quotes, "Authors":authors, "Tags":tags,"Hyperlink": hyperlinks}

    def get_next(self):
        """
        If a NEXT button exists,get the next page's URL 
        """
        next_url = self.response.css("li.next a::attr(href)").extract()
        return next_url

# If NEXT button exists, the loop will scrape quotes, authors, tags and the hyperlinks from the page, transform the URL into  the NEXT page's URL and continue. If it cannot find the NEXT button, the loop will scrape the last page and stop there.
results = []
scr = Quotes(url)

while True:
    time.sleep(1)
    if(scr.get_next()==[]):
        results.append(scr.quote_scraper())
        break
    else:
        results.append(scr.quote_scraper())
        url = base_url + scr.get_next()[0]
        scr = Quotes(url)

print(results)

results

"""#Problem 2"""

def movie_scraper(url,base_url="https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"):
  page = requests.get(url)
  response = TextResponse(body=page.text,url=url,encoding="utf-8")
  titles = response.css("td.titleColumn>a::text").extract()
  year = response.css("td.titleColumn>span.secondaryInfo::text").extract()
  ranking = [i.css("div.velocity::text").extract() for i in response.css("td.titleColumn")]
  rating_td = response.css('td[class = "ratingColumn imdbRating"]')
  rating = [i.css('strong::text').extract() for i in rating_td]
  hyperlink_movie = [base_url + i for i in response.css("td.titleColumn > a::attr(href)").extract()]
  return pd.DataFrame({"Titles":titles,"Year":year,"Hyperlink_movie":hyperlink_movie,"Ranking":ranking,"Rating":rating})

movie_scraper(url="https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm")

"""#Problem 3"""

def books_scraper(url,base_url="http://books.toscrape.com/"):
  page = requests.get(url)
  response = TextResponse(body=page.text,url=url,encoding="utf-8")
  title = response.css("h3 a::attr(title)").extract()
  Price = [i.replace("Â","") for i in response.css("p.price_color::text").extract()]
  stock = [i.css("p.instock.availability::text").extract() for i in response.css("div.product_price")]
  hyperlink_book = [base_url + i for i in response.css("h3 a::attr(href)").extract()]
  hyperlink_image = [base_url + i for i in response.css("img.thumbnail::attr(src)").extract()]
  Rating_books = [i.replace("star-rating","") for i in response.css("p.star-rating::attr(class)").extract()]
  return {"Title":title,"Price":Price,"Stock":stock,"Hyperlink_book":hyperlink_book,"Hyperlink_image":hyperlink_image,"Rating":Rating_books}

#Scrape for the first page only 
books_scraper(url="http://books.toscrape.com/index.html")

#Scrape for all pages(50)
book = []
for i in range(1,51):
  book.append( books_scraper(url = f"http://books.toscrape.com//catalogue/page-{i}.html"))

book

#Scraped as a data frame
def books_scraper(url,base_url="http://books.toscrape.com/"):
  page = requests.get(url)
  response = TextResponse(body=page.text,url=url,encoding="utf-8")
  title = response.css("h3 a::attr(title)").extract()
  Price = [i.replace("Â","") for i in response.css("p.price_color::text").extract()]
  stock = [i.css("p.instock.availability::text").extract() for i in response.css("div.product_price")]
  hyperlink_book = [base_url + i for i in response.css("h3 a::attr(href)").extract()]
  hyperlink_image = [base_url + i for i in response.css("img.thumbnail::attr(src)").extract()]
  Rating_books = [i.replace("star-rating","") for i in response.css("p.star-rating::attr(class)").extract()]
  return pd.DataFrame({"Title":title,"Price":Price,"Stock":stock,"Hyperlink_book":hyperlink_book,"Hyperlink_image":hyperlink_image,"Rating":Rating_books})

#Scrape for the first page only 
books_scraper(url="http://books.toscrape.com/index.html")

#Scrape for all pages(50)
books = []
for i in range(1,51):
  books.append( books_scraper(url = f"http://books.toscrape.com//catalogue/page-{i}.html"))

books
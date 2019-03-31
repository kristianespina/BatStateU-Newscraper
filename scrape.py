import time
from selenium import webdriver
import os
from bs4 import BeautifulSoup
import pandas as pd

CHROME_DRIVER_PATH = os.path.dirname(os.path.realpath(__file__))  + "\chromedriver.exe"

def getNews(url):
    articles = [] # This is where we store articles
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)  # Optional argument, if not specified will search path.
    driver.get(url)
    try:
        old_articles = pd.read_csv('articles.csv')
    except:
        old_articles = None
    while True: 
        main_core = driver.find_element_by_id("main-core")
        article_list = main_core.find_elements_by_tag_name("article")
        for news in article_list:
            title = news.find_element_by_class_name("blog-title").text.strip()
            description = news.find_elements_by_tag_name("p")[0].text.strip()
            date = news.find_element_by_tag_name("time").text
            if old_articles is not None:
                for cache in old_articles['title']:
                    if cache == title:
                        print("No new articles... Stopping...")
                        return articles
                print("New article detected... Appending...")
                articles.append({"description": description,"title": title,"date": date})
            else:
                articles.append({"description": description,"title": title,"date": date})
        try:
            next_button = driver.find_element_by_class_name("pag-next")
            print("Navigating to next page...")
            next_button.click()
        except:
            print("Last page reached...")
            break
    print("Total New Articles: {}".format(len(articles)))
    driver.quit()
    return articles

def main():
    articles = getNews('http://batstate-u.edu.ph/category/news/page/21')
    try:
        article_file = pd.read_csv('articles.csv')
    except:
        article_file = None
    if article_file is None:
        article_file = pd.DataFrame(articles)
    else:

        new_article = pd.DataFrame(articles)
        article_file = pd.concat([new_article, article_file])
        print(article_file)
    article_file.to_csv('articles.csv', index=False)
if __name__ == "__main__":
    main()

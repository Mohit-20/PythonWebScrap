# This Project Based on web scrapping which extract data from website 'https://news.ycombinator.com/' and sort news according to rating so that you dont have to deal with fake news you can use this on a daily basis
# Importing Modules
import requests
from bs4 import BeautifulSoup
import pandas as pd

# using .setoptin because to display all rows and columns in output
pd.set_option('display.max_colwidth', None)  #For max column
pd.set_option('display.max_rows', None)  #For maximum width

# Try And  except to deal with errors
try:
    page_no = int(input('Enter Page Numbers: '))  #Takes input from user i.e page numbers
    if page_no <= 0:
        raise Exception("Pages cannot be negative or 0")  #Raise error because we need positive numbers
except Exception as err:
    print(err)
else:
    story_links = []
    sub_text = []
    for i in range(1, page_no+1):   #Using for loops for extracting data from multiple page numbers
        url = 'https://news.ycombinator.com/news?p='+str(i)
        r = requests.get(url)
        bs = BeautifulSoup(r.content, 'html.parser')  #BeautifulSoup for filtering data
        hn = bs.select('.titlelink')  #using select instead find_all because it automatically select data on basis of class or id
        sc = bs.select('.subtext')
        for j in hn:
            story_links.append(j)
        for j in sc:
            sub_text.append(j)

# Creating function for extracting data from story_links and sub_text and show output as datafame
    def hc_news(hn, sc):
        news = []
        links = []
        rating = []

        for i,j in enumerate(hn):  #using enumarate( in simple word it assign index number after looping) 
            news_data = hn[i].getText()
            link_data = hn[i].get('href', None)
            votes = sc[i].select('.score')
            if(len(votes)):  #usimg len function because in some cases rating will be zero which may cause error
                v = int(votes[0].getText().replace('points', ''))
                news.append(news_data)
                links.append(link_data)
                rating.append(v)
        d = {"News": news, "Links":links, "Rating": rating}

        df = pd.DataFrame(d)  #dataframe
        print(df.sort_values('Rating', ascending=False, ignore_index=True))  #sort value for higher to lower rating

    hc_news(story_links, sub_text)

input()

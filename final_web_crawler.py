from read_write_json import read_json,to_json
import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import urllib
from time import sleep
from urllib.robotparser import RobotFileParser

# checks whether it has access to the url or not.
def polite_checker(robots,url):
    host = urllib.parse.urlparse(url).netloc #host name
    try:
        parser = robots[host]      # checks the value in the dict 
    
    except KeyError:A
        parser = RobotFileParser()
        parser.set_url('https://' + host + '/robots.txt')
        parser.read()
        robots[host] = parser
    return parser.can_fetch('*', url)

# main crawler component

def webspider(CRAWL_LIMIT, seeds):
    visited_url = set()
    queue = seeds
    robots = {}
    crawled = 0
    title_link = [] # publication link
    titles = []
    authors = []    # list of authors
    author_link = []
    pub_year =[]
    abstract =[]

    while queue !=[] and crawled < CRAWL_LIMIT:
        crawled += 1
        url = queue.pop(0)
        visited_url.add(url)

        if not polite_checker(robots, url):
            print('This url is disallowed to access', url)
            continue
        
        sleep(5)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        crawled += 1
        print('fetching.....',url)
        for div in soup.findAll('div',{'class':'result-container'}):
                titles.append(div.h3.a.text)
                
                t_link = div.h3.a.get('href')
                title_link.append(t_link)
                sleep(5)
                soup2 = BeautifulSoup(requests.get(t_link).text, 'html.parser')
                abst = soup2.find('div',{'class':'textblock'})
                
                if abst == None:
                    abstract.append([])
                else:
                    abstract.append(abst.text)
                
                
                pub_year.append(div.find('span',{'class':'date'}).text)
                try:
                    author = div.find_all('a',{'rel':'Person'})
                    a = []
                    alink = []
                    for i in range(len(author)):
                        a.append(author[i].text)

                        alink.append(author[i].get('href'))
                    authors.append(a)
                    author_link.append(alink)
                except Exception:
                         pass

    return titles,title_link,authors,author_link,pub_year,abstract               

def save_indexer(dict_index):
    json_object = json.dumps(dict_index, indent=4)
    with open("inverted_index_f.json", "w") as outfile:
        outfile.write(json_object)


def save_scraped_data(titles,title_link,authors,author_link,pub_year,abstract,Flag=False):
    data =[]
    for i in range(len(titles)):
        if authors[i] != []:
            data.append([{'DocID':i,'Title':titles[i], 'Authors':authors[i], 'Pub_Year':pub_year[i], 'JournalP_link':title_link[i], 'AuthorP_link':author_link[i],'Abstract':abstract[i]}])
    json_object = json.dumps(data, indent=4)
    # writing the scraped data to the local disk and saving it in pickle format to preserve the data structures of the data frame columns.
    if Flag:
        with open("CSM_JournalDetails_o_f.json", "w") as outfile:
            outfile.write(json_object)
    else:
        with open("CSM_JournalDetailsUpdated_f.json", "w") as outfile:
            outfile.write(json_object)

def update_indexer():
    print('checking for updates....')
    update_index = False
    latest_file = "CSM_JournalDetailsUpdated_f.json"
    last_file = "CSM_JournalDetails_o_f.json"
    latest_data = read_json(latest_file)
    last_data = read_json(last_file)

    len_newdata = len(latest_data)
    len_olddata = len(last_data)
    
    if len_newdata == len_olddata:
        updated_data = latest_data[last_data.ne(latest_data).any(axis = 1)]
    
    elif len_newdata > len_olddata:
        updated_data = latest_data[last_data.ne(latest_data).any(axis = 1)]
    
    elif len_newdata < len_olddata:
        updated_data = last_data[latest_data.ne(last_data).any(axis = 1)]
        

    if len(updated_data):
            for i in updated_data['DocID']:
                last_data.iloc[i] = updated_data.iloc[i]  
            to_json(last_data)
            to_json(latest_data,Flag=False)
            update_index = True
            print('updated crawled data on the disk')
    
    if update_index:
        # update the inverted index
        new_index = inverted_indexer(updated_data,dataframe=True)
        index.update(new_index)
        save_indexer(index)
        update_index = False
        print('updated indexer on the disk')
    if not(update_index and len(updated_data)):
        print('no updates found')

    



seed = ['https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell/publications/?page=0',
      'https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell/publications/?page=1',
       'https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell/publications/?page=2',
       'https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell/publications/?page=3',
       'https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell/publications/?page=4']

titles,title_link,authors,author_link,pub_year,abstract = webspider(10,seed)
save_scraped_data(titles,title_link,authors,author_link,pub_year,abstract,Flag=True)
# crawler re-visit policy
# re-vist the webpage weekly once
re_visit = 604800 # num of seconds in 1 week
update_index = False
from inverted_index import inverted_indexer
index = inverted_indexer('CSM_JournalDetails_o_f.json') # builds indexer for first time
save_indexer(index) # save indexer
import time
while True:
    # re-vist the webpage weekly once
    time.sleep(re_visit) # sleep for 1 week

    titles2,title_link2,authors2,author_link2,pub_year2,abstract2 = webspider(10,seed)
    save_scraped_data(titles2,title_link2,authors2,author_link2,pub_year2,abstract2)
    update_indexer() 
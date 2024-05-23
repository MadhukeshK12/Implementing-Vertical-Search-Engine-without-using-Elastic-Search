# information_retrieval
This project was a part of my Informational Retrieval Coursework at Coventry University.
# Task -1 
Develop a vertical search engine (without using Elastic Search) similar to Google Scholar, but specialised to retrieve only papers/books published by a member of the Research Centre for Computational Science and Mathematical Modelling (CSM) at Coventry University with User Interface(UI).

# Solution:
###### Search engine components are crawler, indexer, query processing component. 

1. ### Crawler:
   The crawler cosists a queue which contains urls to be visited, after accessing each url it removes it from the queue and adds new hyperlinks found in the accessed web pages. It removes each url in first in first out fashion.
The crawler starts with initial seed containing a list of urls to be visited and access webpages to collect information like page content, hyperlinks and other information, stores it into a database for later purposes.  For each publication we collect the information on title, authors, publication year, abstract of the journal, links to both author/authors profile page and publication page by scraping respective html tags using BeautifulSoup module. All the collected information is stored on the disk as json file, named as ‘CSM_JournalDetails_o_f. json’.

### Pre-Processing the Crawled Data
Before passing the data to the indexer we pre-process the crawled data and then build the inverted index on the pre-processed data. For each publication we only pre-process the publication title and journal abstract and build inverted index on this pre-processed data.

Pre-processing tasks are as follows and applied in the same order:

•	Tokenization – splits paragraphs and sentences into smaller meaningful words called as tokens. Processing on these tokens is much easier and reduces complexity.

•	Removing numbers – numbers doesn’t hold any useful information in the tokens, so we remove the numbers from each token.

•	Lower-Case Filter – converts all the tokens into lower case to remove the distinction between upper- and lower-case tokens.

•	Punctuation Filter – removes punctuations present in the tokens, as this doesn’t hold any vital information. This helps to treat each text or token equally.

•	Stop-word removal – stop words are the most occurring words, which occurs everywhere in the document. Storing these stop words increases the storage space and also these words doesn’t contribute in matching the query to the document, so we remove it.

•	 Stemming – stemming is the process of reducing the word to its base or root form, so that it helps to match related words to the same stem.

We also apply the same pre-processing steps to the user entered query before further pre-processing of the user query.

Our crawler is polite and follows the rules mentioned in the robots.txt file by reading it. For every request made by the crawler, is delayed by 5 seconds so it does not overload the server by hitting it too fastly. 
Our Crawler is scheduled to run automatically once per week. It re-visits the URL to collect any new information and updates the crawled data on the disk and also updates the inverted index incrementally.
As the rate of change of information is low, we have scheduled the crawler to run automatically once per week. We have implemented this by calling our crawler in infinite while loop, then making it to sleep for 1 week and runs again after 1 week, continues so on .

2. ### Indexer
   
   We have constructed our inverted index from scratch without using Elastic Search. We have used inverted index data structure to build our indexer. We have implemented it by using a python dictionary, where dictionary keys are terms(words) and dictionary values contains postings for each term. Postings are implemented as a python dictionary, where dictionary keys are Document IDs for each term and dictionary values are term frequencies in each document.
   The indexer is only built from the scratch for the first time when webcrawler is called and it is saved on the disk as json file, named as ‘inverted_index_f.json’. When the web crawler see’s new information it incrementally updates the inverted index. 
We implement this by using update function of dictionary to incrementally update the old inverted indexer in the memory. After updating the indexer we save it on the disk.
The fully constructed inverted index is stored on the disk as json file and loaded into the memory while processing the user query.
 Inverted index implemented in python as:
{ term : { DocID : Term Frequency }

3. ### Query Processor
   The query processor component takes the user entered query as input and applies pre-processing to the user query. Then calculates the tf-idf scores for each document containing the user query terms by checking whether or not the term is present in the inverted index. If present calculates idf for each term in the user query and then calculates the tf-idf for each term in the user query. Score for each document is calculated by summing up the tf-idf scores for each document and returns the dictionary containing document ids as keys and score for respective documents as values. The returned dictionary is sorted in decreasing order of score values.

   We perform ranked retrieval by calculating tf-idf of the terms present in both the documents and in the user query.
Before calculating the ranks, we pre-process the user entered query and then calculate the tf-idf. For every token in the pre-processed query, we check whether the token exists in the inverted index or not. If it is present, we calculate the tf-idf as follows:
	TF-IDF = log10(1+tf) X log10(N/df)
tf – term frequency
df – document frequency

Scores for each document is calculated as,
score(q,d) = ∑ TF-IDF

### User interface is implemented by using Python's Flask Web framework.
##### Snapshot:
![image](https://github.com/MadhukeshK12/Implementing-Vertical-Search-Engine-without-using-Elastic-Search/assets/115413028/82ff0a87-e518-4c77-93bc-6fbff0357dbe)


### In Brief:
• Designed and implemented a vertical search engine from scratch to retrieve journal papers from the CSM
department at Coventry University with user interface.

• Conducted pre-processing tasks such as tokenization, lowercasing, stop word removal, and stemming on
scraped data.

• Developed an incremental crawler to update the search index weekly and utilized an inverted index data
structure for efficient indexing. Implemented ranked retrieval using tf-idf scores and developed a userfriendly web interface using Python Flask framework.


# How to Run:
1. Download all the files and save them under one file. 
2. Run final_web_crawler.py in Visual Studio Code  (Requires Internet to Crawl the webpages).

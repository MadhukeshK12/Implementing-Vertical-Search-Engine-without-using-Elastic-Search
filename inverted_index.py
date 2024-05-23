
from text_pre_processor import pre_process
import pandas as pd
import json
from read_write_json import read_json

def inverted_indexer(file,dataframe=False):

    try:
        indexer = read_json('inverted_index_f.json',index=True)
        if len(indexer):
            print('loaded indexer from disk')
            return indexer
    except Exception:
        pass
    print('Building indexer for the first time')
    if not dataframe:
        with open(file, 'r') as openfile:
        # Reading from json file
            json_object = json.load(openfile)
        df = pd.DataFrame()
        for i in json_object:
            df=df.append(i,ignore_index=True)
        count = 0
        for i in df['Authors']:
            if i == []:
                df=df.drop(count)
            count+=1

    else:
        df = file
    dict_index = {}
    series_title = df['Title']
    series_abstract = df['Abstract']
    DocID = list(df.index)
    count = 0
    for doc in DocID:
        words_title = pre_process(series_title[doc]) 
        for term in words_title:
            count+=1
            if term not in dict_index.keys():
                dict_index[term] = {doc:count}
            elif term in dict_index.keys():
                try:
                    dict_index[term][doc]+=count
                except KeyError:
                    dict_index[term].update({doc:count})
            count = 0
         
        words_abstract = pre_process(series_abstract[doc])
        for term in words_abstract:
            count+=1
            if term not in dict_index.keys():
                dict_index[term] = {doc:count}
            elif term in dict_index.keys():
                try:
                    dict_index[term][doc]+=count
                except KeyError:
                    dict_index[term].update({doc:count})
            count = 0
        count = 0

        
    return dict_index 

# a=inverted_indexer('CSM_JournalDetails_o2.json')
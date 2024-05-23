from text_pre_processor import pre_process
from inverted_index import inverted_indexer
import pandas as pd
from read_write_json import read_json,to_json
index = inverted_indexer('CSM_JournalDetails_o_f.json')

             
import math   
def inverse_doc_freq(index,file,terms):
    idf_dict = {}
    df = read_json(file)
    N = len(df)
    df = 0
    
    for term in terms:
        if term in index.keys():
            df = len(index[term])
            idf_dict[term] = math.log10((N/df))
        df = 0
    
    return idf_dict

def tfXidf(tf,idf):
    tf_idf = {k:v for k,v in tf.items() if k in idf.keys()}
    for term in tf_idf.keys():
        for doc in tf_idf[term].keys():
            tf_idf[term][doc]= math.log10(1+tf[term][doc]) * idf[term]
    return tf_idf
            
def score(tfidf):
    scores = {}
    
    for term in tfidf.keys():
        for doc in tfidf[term].keys():
            try:
                scores[doc]+= tfidf[term][doc]
            except KeyError:
                scores[doc] = tfidf[term][doc]
    
    return dict(sorted(scores.items(),key = lambda x: x[1], reverse=True))
                
def similarity(index,file,terms):
    b=inverse_doc_freq(index, file,terms)
    c=tfXidf(index,b)
    return score(c)
def result(query):
    sim = similarity(index,'CSM_JournalDetails_o_f.json',pre_process(query))
    df_final = read_json('CSM_JournalDetails_o_f.json')
    result_df = pd.DataFrame()
    for doc in sim.keys():
        result_df = result_df.append(df_final.iloc[doc])
    return result_df,sim
if __name__ == '__main__':   
    result(['efficaci','covid'])
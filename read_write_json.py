import json
import pandas as pd
def save_indexer(dict_index):
    df=pd.DataFrame(columns=['Terms','DocID_tf'])
    data = []
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

def read_json(file,index = False):
    with open(file, 'r') as openfile:
    # Reading from json file
        json_object = json.load(openfile)
    if index:
        d=json_object
        for i in d.keys():
            d[i] = {int(k):v for k,v in d[i].items()}
        return d
        
    final_DataFrame = pd.DataFrame()
    for i in json_object:
        final_DataFrame=final_DataFrame.append(i,ignore_index=True)
    count = 0
    # for i in final_DataFrame['Authors']:
    #     if i == []:
    #         final_DataFrame=final_DataFrame.drop(count)
    #     count+=1
    return final_DataFrame

def to_json(df,Flag=True):
    save_scraped_data(df['Title'],df['JournalP_link'],df['Authors'],df['AuthorP_link'],df['Pub_Year'],df['Abstract'],Flag=True)
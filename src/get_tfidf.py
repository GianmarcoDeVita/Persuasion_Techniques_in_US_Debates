import argparse
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import numpy as np
from ruamel.yaml import YAML
import pandas as pd

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
    
def get_tfidf(opt, params):
    dest_folder = opt.dest_folder
    number_to_keep = params['tfidf']['number_to_keep']
    #create folder if it does not exist
    os.makedirs(dest_folder, exist_ok=True)
    #get json files in data folder
    files = [f for f in os.listdir(opt.data_folder) if f.endswith('.json')]
    for file in files:

        results = dict()

        #read json file
        with open(os.path.join(opt.data_folder,file), 'r') as f:
            data = json.load(f)
        #get all the parties
        parties = data.keys()
        for party in parties:
            #get all the debates
            corpus = data[party].values()
            vectorizer = TfidfVectorizer(stop_words = 'english')
            X = vectorizer.fit_transform(corpus)
            out = vectorizer.get_feature_names_out()
            feature_array = np.array(out)
            count_lst = X.toarray().sum(axis=0)

            vocab_df = pd.DataFrame((zip(feature_array,count_lst)),
                          columns= ["vocab","tfidf_value"])

            vocab_df.sort_values(by="tfidf_value",ascending=False, inplace=True)
            #convert the df to a list
            tfid_dict = vocab_df.to_dict(orient='records')
       
            results[party] = tfid_dict[:number_to_keep]


        #save file
        with open(opt.dest_folder + f"{file}", 'w') as f:
            json.dump(results, f,ensure_ascii=False,indent=4, cls=NumpyEncoder)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_folder', type=str, default='data/no_stop_words', help='source')
    parser.add_argument('--dest_folder', type=str, default='data/tfidf', help='destination')
    parser.add_argument('--params', type=str, default='params.yaml', help='params')  # file/folder, 0 for webcam

    opt = parser.parse_args()
    return opt

def main():
    opt = parse_arguments()
    with open(opt.params) as f:
        yaml = YAML(typ="safe")
        params = yaml.load(f) 
    get_tfidf(opt, params)

    

if __name__ == '__main__':
    main()
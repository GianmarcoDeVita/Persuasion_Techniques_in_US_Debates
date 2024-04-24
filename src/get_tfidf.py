import argparse
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
    
def get_tfidf(opt):
    dest_folder = opt.dest_folder
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
            vectorizer = TfidfVectorizer()
            X = vectorizer.fit_transform(corpus)
            out = vectorizer.get_feature_names_out()
            print(out)
            #asdfs
            results[party] = out
        #save file
        with open(opt.dest_folder + f"{file}.json", 'w') as f:
            json.dump(results, f,  cls=NumpyEncoder)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_folder', type=str, default='data/no_stop_words', help='source')
    parser.add_argument('--dest_folder', type=str, default='data/tfidf', help='destination')
    opt = parser.parse_args()
    return opt

def main():
    opt = parse_arguments()
    get_tfidf(opt)

    

if __name__ == '__main__':
    main()
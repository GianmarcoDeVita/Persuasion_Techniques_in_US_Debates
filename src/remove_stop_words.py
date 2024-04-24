import argparse
import json
import os
import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def remove_stop_words(opt):
    nltk.download('stopwords')
    nltk.download('punkt')
    stop_words = set(stopwords.words('english'))
    dest_folder = opt.dest_folder
    #create folder if it does not exist
    os.makedirs(dest_folder, exist_ok=True)
    #get json files in data folder
    files = [f for f in os.listdir(opt.data_folder) if f.endswith('.json')]
    for file in files:
        #read json file
        with open(os.path.join(opt.data_folder, file), 'r') as f:
            data = json.load(f)
        #get all the categories
        #categories = data["persuasion_technique_category"].unique()
        
        #iterate over categories
        #for category in categories:
        results = {}
        #filter by category
        #data_category = data[data["persuasion_technique_category"] == category]
        #iterate over parties
        for party in data.keys():
            results[party] = {}
            for debate in data[party].keys():
            #filter by party
                word_tokens = word_tokenize(data[party][debate])
                # converts the words in word_tokens to lower case and then checks whether 
                #they are present in stop_words or not
                filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
                #with no lower case conversion
                filtered_sentence = []
                
                for w in word_tokens:
                    if w not in stop_words:
                        filtered_sentence.append(w)

                results[party][debate] = " ".join(filtered_sentence)
                #save file
        with open(os.path.join(dest_folder,file), 'w') as f:
            json.dump(results, f)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_folder', type=str, default='data/persuasion_files', help='source')
    parser.add_argument('--dest_folder', type=str, default='data/no_stop_words', help='destination')
    opt = parser.parse_args()
    return opt

def main():
    opt = parse_arguments()
    remove_stop_words(opt)

    

if __name__ == '__main__':
    main()
import argparse
import pandas as pd
import json
import os
#fix seed for pandas sampling
def create_persuasion_files(opt):
    data = pd.read_csv(opt.data)
    #get all the categories
    categories = data["persuasion_technique_category"].unique()
    dest_folder = opt.dest_folder
    #create folder if it does not exist
    os.makedirs(dest_folder, exist_ok=True)
    #iterate over categories
    for category in categories:
        
        results = {}
        #filter by category
        data_category = data[data["persuasion_technique_category"] == category]
        #iterate over parties
        for party in data_category["party"].unique():
            results[party] = {}
            #filter by party
            data_party = data_category[data_category["party"] == party]
            #iterate over debates
            for debate in data_party["debate"].unique():
                results[party][debate] = ""
                #filter by debate
                data_debate = data_party[data_party["debate"] == debate]
                #iterate over rows
                for index, row in data_debate.iterrows():
                    results[party][debate] += row["text"] + "\n"
        #save file
        with open(opt.dest_folder + "/" + category + ".json", 'w') as file:
            json.dump(results, file)
        
                


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='data/results.csv', help='source')
    parser.add_argument('--dest_folder', type=str, default='data/persuasion_techniques', help='destination folder')

    opt = parser.parse_args()
    return opt

def main():
    opt = parse_arguments()
    create_persuasion_files(opt)

    

if __name__ == '__main__':
    main()
import argparse
import json
import os
import pandas as pd

def unify_string_format(string):
    return string.lower().replace(" ", "_").replace('/', '-').replace('_or_', '-').replace('_-_', '-')

def merge_results(opt):
    #read categories file
    with open(opt.categories_file, 'r') as file:
        categories = json.load(file)
    #put all the keys of category, that is a dict, in lowestring
    #categories = {k.lower(): v for k, v in categories.items()}
    #put all the keys substituting spaces by underscores
    categories = {unify_string_format(k): v for k, v in categories.items()}
    #get all the json files in the source folder
    files = [f for f in os.listdir(opt.source_folder) if f.endswith('.json')]
    #create new dataframe
    data = pd.DataFrame(columns=["year", "date","debate", "candidate", "party", "incumbent", "party_incumbent", "winner", "home_state", "persuasion_technique", "persuasion_technique_category", "persuasion_percentage_over_txt", "score"])
    #read all the json files
    for file in files:
        with open(opt.source_folder + file, 'r') as file:
            json_data = json.load(file)
            for candidate in json_data["candidates"]:
                for annotation_k, annotation_v in candidate["annotations"]["entities"].items():
                    for annotation in annotation_v:
                        key = unify_string_format(annotation_k)
                        len_persuasion = annotation["indices"][1] - annotation["indices"][0]
                        txt_len = len(candidate["text"])
                        row = {
                            "year": json_data["year"],
                            "date": json_data["date"],
                            "debate": json_data["debate_name"],
                            "candidate": candidate["name"],
                            "party": candidate["party"],
                            "incumbent": candidate["incumbent"],
                            "party_incumbent": candidate["party_incumbent"],
                            "winner": candidate["winner"],
                            "home_state": candidate["home_state"],
                            "persuasion_technique": annotation_k,
                            "persuasion_technique_category": categories[key],
                            "annotations": candidate["annotations"],
                            "persuasion_percentage_over_txt": len_persuasion/txt_len,
                            "score": annotation["score"]
                        }
                        data.loc[len(data)] = row
                #add a column containing how many uniques debates there are in the year
    data["debate_count"] = data.groupby("year")["debate"].transform("nunique")
    data['date'] = pd.to_datetime(data['date'],format='%Y-%m-%d')
 
    data.sort_values(by='date', inplace=True)


    #save output csv
    data.to_csv(opt.dest, index=False)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_folder', type=str, default='data/speeches/', help='source')
    parser.add_argument('--dest', type=str, default='data/annotations.csv', help='destination')
    parser.add_argument('--categories_file', type=str, default='data/categories.json', help='categories file')

    opt = parser.parse_args()
    return opt

def main():
    opt = parse_arguments()
    merge_results(opt)

    
if __name__ == '__main__':
    main()
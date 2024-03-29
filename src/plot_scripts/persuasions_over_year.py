import os
import pandas as pd
from ruamel.yaml import YAML
import argparse
#fix seed for pandas sampling
import seaborn as sns
import matplotlib.pyplot as plt

def persuasion_over_year(opt,params):
    params = params["plots"]
    plots_folder = os.path.join(params['plots_folder'],"persuasions_over_year")
    df=pd.read_csv(opt.data)
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(20, 10))
    sns.color_palette("hls", 8)


    if params["percentage_plot_folder"]:
        percentage_plots_folder = os.path.join(plots_folder, params["percentage_plot_folder"])
        os.makedirs(percentage_plots_folder, exist_ok=True)
        df["persuasion_percentage_over_txt"] = df["persuasion_percentage_over_txt"]/df["debate_count"]
        hue_order = df.groupby('persuasion_technique_category')["persuasion_technique_category"].first().sort_values().index

        if params["single_plot"]:
            #divide persuasion_percentage_over_txt by debate_count
            #iterate over values of party
            os.makedirs(os.path.join(percentage_plots_folder, "single_plots"), exist_ok=True)
            for party in df["party"].unique():
                #filter by party
                df_party = df[df["party"] == party]
                #create plot
                ax = sns.barplot(x="year", y="persuasion_percentage_over_txt", hue = "persuasion_technique_category",data=df_party, estimator='sum', hue_order=hue_order)
                #save plot
                ax.set_title(party)

                ax.get_figure().savefig(os.path.join(percentage_plots_folder, "single_plots",party + ".png"))
                ax.get_figure().clear()

        if params["merged_plot"]:
            #create subplot for every party
            fig, axs = plt.subplots(len(df["party"].unique()), 1, figsize=(20, 20))
            #iterate over values of party
            for i, party in enumerate(df["party"].unique()):
                #filter by party
                df_party = df[df["party"] == party]
                #create plot
                ax = sns.barplot(x="year", y="persuasion_percentage_over_txt", hue = "persuasion_technique_category",data=df_party, estimator='sum', ax=axs[i], hue_order=hue_order)
                #set title
                ax.set_title(party)
            #save plot
            fig.savefig(os.path.join(percentage_plots_folder, "merged.png"))
            ax.get_figure().clear()


    if params["count_plot_folder"]:
        count_plots_folder = os.path.join(plots_folder, params["count_plot_folder"])
        os.makedirs(count_plots_folder, exist_ok=True)

        if params["single_plot"]:
            #iterate over values of party
            os.makedirs(os.path.join(count_plots_folder, "single_plots"), exist_ok=True)

            for party in df["party"].unique():
                #filter by party
                df_party = df[df["party"] == party]
                #create plot, the count should be divided by the number of debates
                ax = sns.countplot(x="year", hue = "persuasion_technique_category",data=df_party, hue_order=hue_order)

                #save plot
                ax.set_title(party)
                ax.get_figure().savefig(os.path.join(count_plots_folder, "single_plots",party + ".png"))
                ax.get_figure().clear()

        if params["merged_plot"]:
            #create subplot for every party
            fig, axs = plt.subplots(len(df["party"].unique()), 1, figsize=(20, 20))
            #iterate over values of party
            for i, party in enumerate(df["party"].unique()):
                #filter by party
                df_party = df[df["party"] == party]
                #create plot
                ax = sns.countplot(x="year", hue = "persuasion_technique_category",data=df_party, ax=axs[i], hue_order=hue_order)
                #set title
                ax.set_title(party)
            #save plot
            fig.savefig(os.path.join(count_plots_folder, "merged.png"))



def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='data/results.csv', help='source')
    parser.add_argument('--params', type=str, default='params.yaml', help='params')
    opt = parser.parse_args()
    
    return opt

def main():
    opt = parse_arguments()
    with open(opt.params) as f:
        yaml = YAML(typ="safe")
        params = yaml.load(f) 
    persuasion_over_year(opt,params)

if __name__ == '__main__':
    main()
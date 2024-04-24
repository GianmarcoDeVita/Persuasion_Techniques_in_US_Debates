import os
import pandas as pd
from ruamel.yaml import YAML
import argparse
#fix seed for pandas sampling
import seaborn as sns
import matplotlib.pyplot as plt

def persuasion_over_year(opt,params):

    params = params["plots"]
    plots_folder = os.path.join(params['plots_folder'],"recourse_to_technique_over_year")
    df=pd.read_csv(opt.data)
    sns.set_theme(style="whitegrid")
    sns.color_palette("hls", 8)
    hue_order = ['Democrat', 'Republican']
    hue_palette = {'Democrat': '#00AEF3', 'Republican': '#E81B23'}
    df = df.rename(columns = {"party":"Party", "year":"Year"})


    if params["percentage_plot_folder"]:
        plt.figure(figsize=(16, 9))
        df["persuasion_percentage_over_txt"] = df["persuasion_percentage_over_txt"]/df["debate_count"]

        percentage_plots_folder = os.path.join(plots_folder, params["percentage_plot_folder"])
        os.makedirs(percentage_plots_folder, exist_ok=True)
        if params["single_plot"]:
            os.makedirs(os.path.join(percentage_plots_folder, "single_plots"), exist_ok=True)

            #divide persuasion_percentage_over_txt by debate_count
            #iterate over values of party
            for category in df["persuasion_technique_category"].unique():
                #filter by party
                df_category = df[df["persuasion_technique_category"] == category]
                #create plot
                #s = df_category['date'].value_counts(ascending=True)           # compute counts by class

                ax = sns.barplot(x="Year", y="persuasion_percentage_over_txt", hue = "Party",data=df_category, estimator='sum', hue_order=hue_order, palette=hue_palette)
                #save plot
                plt.legend(fontsize = "21")

                ax.set_title(category)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

                ax.get_figure().savefig(os.path.join(percentage_plots_folder, "single_plots",category.replace(" ", "_") + ".eps"), transparent=True)
                ax.get_figure().clear()

        if params["merged_plot"]:
            #create subplot in a grid 3x2 for every category
            fig, axs = plt.subplots(3, 2, figsize=(16*2, 9*3))
            #iterate over values of party
            for i, category in enumerate(df["persuasion_technique_category"].unique()):
                #filter by party
                df_category = df[df["persuasion_technique_category"] == category]
                #create plot

                ax = sns.barplot(x="Year", y="persuasion_percentage_over_txt", hue = "Party",data=df_category, estimator='sum', ax=axs[i//2, i%2], hue_order=hue_order, palette=hue_palette)
                #set title
                ax.set_title(category)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

            #save plot
            fig.savefig(os.path.join(percentage_plots_folder, "merged.eps"), transparent=True)
            ax.get_figure().clear()
        
    if params["count_plot_folder"]:
        plt.figure(figsize=(16, 9))

        count_plots_folder = os.path.join(plots_folder, params["count_plot_folder"])
        os.makedirs(count_plots_folder, exist_ok=True)

        if params["single_plot"]:
            os.makedirs(os.path.join(count_plots_folder, "single_plots"), exist_ok=True)

            #iterate over values of party
            for category in df["persuasion_technique_category"].unique():
                #filter by party
                df_category = df[df["persuasion_technique_category"] == category]

                #create plot
                ax = sns.countplot(x="Year", hue = "Party",data=df_category, hue_order=hue_order, palette=hue_palette)
                #save plot
                plt.legend(fontsize = "21")

                ax.set_title(category)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

                ax.get_figure().savefig(os.path.join(count_plots_folder, "single_plots",category.replace(" ", "_") + ".eps"), transparent=True)
                ax.get_figure().clear()

        if params["merged_plot"]:
            #create subplot in a grid 3x2 for every category
            fig, axs = plt.subplots(3, 2, figsize=(16*2, 9*3))
            #iterate over values of party
            for i, category in enumerate(df["persuasion_technique_category"].unique()):
                #filter by party
                df_category = df[df["persuasion_technique_category"] == category]

                #create plot
                ax = sns.countplot(x="Year", hue = "Party",data=df_category, ax=axs[i//2, i%2], hue_order=hue_order, palette=hue_palette)
                #set title
                ax.set_title(category)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

            #save plot
            fig.savefig(os.path.join(count_plots_folder, "merged.eps"), transparent=True)
            ax.get_figure().clear()
            

            

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
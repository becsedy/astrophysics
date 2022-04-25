# -*- coding: utf-8 -*-
"""
Yash R. Bhora
DS2001 Practicum Final Project
Relative Frequencies of Stellar Classes at Different Radii from Earth
April 8, 2022
stellar_distribution.py

Description: The purpose of this program is to create a GIF animation that 
illustrates the relative frequency of different stellar classes, classified
by K-means, at different radii (in lightyears) away from the Earth. The program
creates a bar chart depicting the relative frequencies and the GIF animation
shows how the chart varies as radii increase.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio

FILENAME = "astronomy_calculations3.csv"
# Colors correspond to K-means cluster plot of different Classes
COLORS = ["plum", "lightcoral", "skyblue", "sandybrown", "limegreen"]
LABELS = ["Class A", "Class B", "Class C", "Class D", "Class E"]

def read_csv(filename):
    """ Function: read_csv
        Parameters: Name of CSV file to be read (string)
        Returns: dataframe with only distance and cluster color columns
    """
    df = pd.read_csv(filename)
    df = df.rename(columns={"Distance\n": "distance", "Cluster": "cluster"})
    df = df[["distance", "cluster"]]
    
    return df

def cluster_count(df, threshold):
    """ Function: cluster_count
        Paremeters: dataframe with data, list of clusters, light year 
        threshold (float)
        Returns: list with percent distribution of each cluster
    """
    df_filt = df[df["distance"] < threshold]
    
    # Dataset contains different labels for the classes and so the data is 
    # adjusted accordingly.
    df_filt = df_filt.replace('red', 'Class D')
    df_filt = df_filt.replace('fuchsia', 'Class A')
    df_filt = df_filt.replace('orange', 'Class C')
    df_filt = df_filt.replace('green', 'Class B')
    df_filt = df_filt.replace('blue', 'Class E')
    
    # The pandas series is sorted by index to keep the order the same in the 
    # plots. It contains relative frequencies of the stellar classes.
    clust_counts = df_filt["cluster"].value_counts(normalize=True).sort_index()
    
    return clust_counts
    
    
def main():
    df = read_csv(FILENAME)
    ninety_q = df["distance"].quantile(0.9) # 90th Quantile of all stars
    ten_q = df["distance"].quantile(0.1) # 10th Quantile of all stars
    
    # Quantiles are selected to avoid extremes that may skew data
    # 20 threshold values are selected for plotting
    thresholds = np.linspace(round(ten_q), round(ninety_q), 20)
    
    # Variables that keep track of filenames for GIF animation
    count = 0
    filenames = []
    
    # Iterating through each threshold to produce corresponding bar chart
    for threshold in thresholds:
        filename = "hist" + str(count) + ".png"
        clust_c = cluster_count(df, threshold)
        
        plt.figure(dpi = 200)
        cols = clust_c.index[:len(COLORS)]
        plt.bar(cols, clust_c[:len(COLORS)], color = COLORS )
        plt.ylim(0, 1)
        plt.title("Cluster Distributions Within Radius < " + str(round(threshold)) + " ly")
        plt.xlabel("Cluster Class")
        plt.ylabel("Relative Frequency")
        plt.savefig(filename)
        plt.show()
        count += 1
        
        # To adjust for duration of frames in the GIF animation
        if count == 0:
            filenames += [filename] * 10
        else:
            filenames += [filename] * 3
    
    # Turn figures to GIF
    with imageio.get_writer('stellar_distributions.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
    
main()

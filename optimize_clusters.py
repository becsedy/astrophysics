# -*- coding: utf-8 -*-
"""
Yash R. Bhora
DS2001 Practicum Final Project
Optimizing K-means Clusters using Within Cluster Sum of Squares
April 8, 2022
optimize_clusters.py

Description: There are two primary purposes for this program: 
    1) generate plots with different amounts of clusters to create a 
    GIF animation. 
    2) to determine the optimum amount of clusters for our data using Within
    Cluster Sum of Squares (WCSS).

The program does in the listed order. It first loops through creating a plot
of the clusters for 1 to 11 clusters. Whilst it is looping through creating
the different cluster quantities, it stores the sum of squares data in a list
called 'wcss' which is later used to generate a plot that compares the number
of clusters to the corresponding sum of squares. The elbow method is then used
to determine the optimum number of clusters, which came out to be around 5.

The purpose of the GIF animation is to visualize how the clustering changes as
the number of clusters increase.

Code was inspired from "K-means Clustering Python Example" by Cory Malkin from
towardsdatascience.com

"""
import numpy as np
import csv
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import imageio
import seaborn as sns

PALETTE = sns.color_palette(None, 11)
FILENAME = "astronomy_calculations.csv"
ITERATIONS = range(1, 11)

def read_data(file):
    """ Function: read_data; reads the third and fourth column of csv where
                  lie the data of interest(color and absolute magnitude).
        Parameters: file (string); name of the file
        Returns: A numpy array of tuples containing two data points 
        (color, abs mag)
    """
    X = []
    with open(file, "r") as csvfile:
        next(csvfile)
        data = csv.reader(csvfile)
        
        for row in data:
            tup = []
            tup.append(float(row[2]))
            tup.append(float(row[3]))
            X.append(tup)
    
    return np.array(X)

def main():
    X = read_data(FILENAME)
    
    wcss = [] # List storing wcss values for each iteration of clusters
    filenames = [] # List storing the names of png files depicting plots
    
    for i in ITERATIONS:
        # Running kmeans clustering on dataset
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=len(X),
                        n_init=10, random_state=0)
        y_kmeans = kmeans.fit_predict(X)
        
        wcss.append(kmeans.inertia_) # kmeans.inertia returns sum of squares
        plt.figure(dpi = 200)
        
        # For loop that plots each cluster on the current figure
        for j in range(i):
            plt.plot(X[y_kmeans == j, 0], X[y_kmeans == j, 1], "o", 
                     ms = 0.05, color = PALETTE[j])
        
        # Plotting each centroid of the clusters
        plt.plot(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1],
                 "o", ms = 2, c = "black", label = "Centroids")
        plt.xlabel("Color (B-V) (nm)")
        plt.ylabel("Luminosity (Solar Units) (log base 10)")
        plt.title("Color VS Luminosity, Clusters = " + str(i))
        
        filename = "Clusters_" + str(i) + ".png"
        filenames += 5 * [filename]
        
        plt.savefig(filename)
        plt.show()
        
    # Turn figures to GIF
    with imageio.get_writer('clusters.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
    
    # Plotting WCSS
    plt.plot(ITERATIONS, wcss)
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()
    
main()

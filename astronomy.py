# importing necessary libraries
import math
import matplotlib.pyplot as plt
import random as rnd

# rows straight from file
rows = []
# setting up lists to be iterated later
columns = []
absolutes = []
centroids = []
point_colors = []
closest_centroid = []
colors = ["red", "blue"]
clusters = len(colors)

FILE_NAME = "astronomy_calculations.csv"

def absolute(Vmag, plx):
    '''
    Function: absolute(Vmag, plx)
    Inputs: Vmag (apparent magnitude); plx (parallax); both floats
    Returns: The absolute magnitude of a star with those Vmag and plx
            values
    '''
    if abs(plx) != 0:
        return (15 - Vmag - 5 * math.log10(abs(plx))) / 2.5
    else:
        return 0

def luminosity(absolute):
    '''
    Function: luminosity(absolute)
    Inputs: absolute (absolute magnitude), a float
    Returns: The luminosity of a star with that given absolute magnitude
    '''
    return 10 ** (absolute / -2.5) * 3.0128 * 10 ** 28

def distance(color, cent_color, Vmag, cent_Vmag):
    '''
    Function: distance(color, cent_color, Vmag, cent_Vmag)
    Inputs: color (color a point), cent_color (color of the centroid),
            Vmag (app. magnitude of a point), cent_Vmag
            (app. mag. of the centroid); all floats
    Returns: Euclidean distance between the point and the centroid
    '''
    return ((color - cent_color)** 2 + (Vmag - cent_Vmag) ** 2) ** 0.5

def average(lst):
    '''
    Function: avg(lst)
    Inputs: lst, a list
    Returns: The average value of the coordinates in the list
    '''
    avgs = []
    for coordinate in range(len(lst[0])):
        sum = 0
        for list_pos in range(len(lst)):
            # sums up the values in the list
            sum += lst[list_pos][coordinate]
        # divides by the length of the list
        avg = sum / len(lst)
        avgs.append(avg)
    return avgs

def main():
    last_centroids = []
    # opening, reading, and extracting data from the text file
    with open(FILE_NAME, "r") as infile:
        while True:
            row = infile.readline()
            if row == "":
                break
            else:
                rows.append(row)
                
    # separates rows into lists
    for i in range(len(rows)):
        rows[i] = rows[i].split(sep = ",")
    
    # remove headers
    rows.pop(0)
    
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            rows[i][j] = float(rows[i][j])
    
    # transposes rows into columns, easier to work with
    for j in range(len(rows[0])):
        column = []
        for i in range(len(rows)):
            column.append(rows[i][j])
        columns.append(column)
    
    # defines number of stars as the number of rows in the dataset
    num_stars = len(columns[0])
    
    # resolution of the graph
    plt.figure(dpi = 500)
    
    # for each of the clusters...
    for i in range(clusters):
        # seeds each cluster with a randomly selected starting point
        x = rnd.randint(1, num_stars)
        centroids.append([columns[2][x], columns[3][x]])

    # while the centroids are still converging...
    while centroids != last_centroids:
        point_colors = []
        # clearing the coordinates of the last centroids
        for l in range(len(last_centroids) - 1, -1, -1):
            last_centroids.pop(l)

        # computing the distance of each star to each centroid
        for i in range(num_stars):
            distances = []
            for j in range(clusters):
                # add the distance to this star to each centroid
                distances.append(distance(columns[2][i], centroids[j][0], 
                                          columns[3][i], centroids[j][1]))
            # minimum distance = closest centroid
            closest_centroid = distances.index(min(distances))
            # assigns that star the color of the closest centroids
            point_colors.append(colors[closest_centroid])
        
        # preparing to iterate by setting centroid values to
        # last centroid values
        for l in range(len(centroids)):
            last_centroids.append(centroids[l])
        
        # preparing to iterate by clearing centroid values
        for m in range(clusters - 1, -1, -1):
            centroids.pop(m)
        
        # computing the centroid of each new cluster
        for c in range(clusters):
            points = []
            for p in range(num_stars):
                if point_colors[p] == colors[c]:
                    points.append([columns[2][p], columns[3][p]])
            centroids.append(average(points))
    
    # after the centroids have converged:    
    # graphs each point, coloring it the color of the closest centroid
    for i in range(num_stars):
        plt.xlabel("Color (B-V)")
        plt.ylabel("Absolute Magnitude")
        plt.plot(columns[2][i], columns[3][i], 
                 "o", color = point_colors[i], ms = 0.05)
        
    # graphs centroids
    for i in range(clusters):
        plt.plot(centroids[i][0], centroids[i][1], "s", 
                 color = "black", ms = 3)

main()
"""
DS 2000

Krishi Patel

File Name:3dplot

Date:
"""

filename = "astrophysics_calculations.csv"
import csv
%matplotlib qt
import matplotlib.pyplot as plt





def read_data(filename):
    ''' Function: read_data
        Parameters: filename (string) for a txt file
        Returns: list of x's, y's, z's, and cluster colors
    '''
    x = []
    y = []
    z = []
    clusters = []
    
    with open(filename, "r") as infile:
        reader = csv.reader(infile, delimiter= ",")
        next(reader)
        for row in reader:
                x.append(float(row[6]))
                y.append(float(row[7]))
                z.append(float(row[8]))
                clusters.append((row[10]))
                
    return x, y, z, clusters



def plot(x, y, z, clusters):
    ''' Function: plot
        Parameters: list of x's, y's, z's, and clusters 
        Returns: nothing, just generates a plot
    '''
    fig = plt.figure() 
    ax = fig.add_subplot(projection='3d')
    plt.xlim(-3000, 3000)
    plt.ylim(-3000, 3000)
    ax.set_zlim(-3000, 3000)
    for i in range(0,1000):
        if clusters[i] == 'red':
            ax.scatter(x[i], y[i], z[i], c = "#f4a460", s=3)
        if clusters[i] == 'blue':
            ax.scatter(x[i], y[i], z[i], c = "#32CD32", s=3)    
        if clusters[i] == 'orange':
            ax.scatter(x[i], y[i], z[i], c = "#87ceeb", s=3) 
        if clusters[i] == 'fuchsia':
            ax.scatter(x[i], y[i], z[i], c = "#f08080", s=3)   
        if clusters[i] == 'green' and z[i]< 1000:
            ax.scatter(x[i], y[i], z[i], c = "#673147", s=3)
   
    plt.show()

def main():
    # take the data from the file
    x, y, z, clusters = read_data(filename)
    
    # plot data
    plot(x, y, z, clusters)
            

main()

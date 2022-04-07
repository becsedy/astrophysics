# importing necessary libraries
import math
import matplotlib.pyplot as plt
import random as rnd
import csv
import numpy as np

# rows straight from file
rows = []
# setting up lists to be iterated later
absolutes = []
xs = []
ys = []
zs = []

FILE_NAME = "hipparcos-voidmain.csv"
VMAG_COLUMN = 5
RA_COLUMN = 8
DE_COLUMN = 9
PLX_COLUMN = 11
COLOR_COLUMN = 37

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

def getx(plx, RA, DE):
    theta = np.pi / 2 - np.radians(DE)
    return plx * np.sin(theta) * np.cos(RA)

def gety(plx, RA, DE):
    theta = np.pi / 2 - np.radians(DE)
    return plx * np.sin(theta) * np.cos(RA)

def getz(plx, RA, DE):
    theta = np.pi / 2 - np.radians(DE)
    return plx * np.cos(theta)

def main():
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
        
    # removes incomplete data
    for i in range(len(rows) - 1, -1, -1):
        for j in [VMAG_COLUMN, COLOR_COLUMN, PLX_COLUMN]:
            if rows[i][j] == "" or rows[i][j] == None:
                rows.pop(i) 
    
    # keeping only Vmag, RA, DE, Plx, and Color data            
    for i in range(len(rows)):
        for j in range(len(rows[i]) - 1, -1, -1):
            if j not in [VMAG_COLUMN, RA_COLUMN,
                         DE_COLUMN, PLX_COLUMN, COLOR_COLUMN]:
                rows[i].pop(j)
            elif i != 0:
                rows[i][j] = float(rows[i][j])
    
    # calculate x, y, z:
    for i in range(len(rows)):
        if i == 0:
            xs.append("x")
            ys.append("y")
            zs.append("z")
        else:
            xs.append(getx(rows[i][3], rows[i][1], rows[i][2]))
            ys.append(gety(rows[i][3], rows[i][1], rows[i][2]))
            zs.append(getz(rows[i][3], rows[i][1], rows[i][2]))
    
    # adds absolute magnitude data
    for i in range(len(rows)):
        if i == 0:
            absolutes.append("Abs Mag")
        else:
            absolutes.append(absolute(rows[i][0], rows[i][1]))
            
    for i in range(len(rows)):
        rows[i].append(absolutes[i])
        rows[i].append(xs[i])
        rows[i].append(ys[i])
        rows[i].append(zs[i])
              
    with open("astronomy_calculations.csv", "w", newline = "") as outfile:
        writer = csv.writer(outfile)
        for i in range(len(rows)):
            writer.writerow(rows[i])

main()
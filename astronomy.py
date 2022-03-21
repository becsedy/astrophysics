import math
import matplotlib.pyplot as plt

rows = []
columns = []
absolutes = ["Vmag_abs"]

def absolute(Vmag, plx):
    return (15 - Vmag - 5 * math.log10(plx)) / 2.5

def main():
    with open("HIP_star_data.txt", "r") as infile:
        while True:
            row = infile.readline()
            if row == "":
                break
            else:
                rows.append(row)
            
    for i in range(len(rows)):
        rows[i] = rows[i].split(sep = " ")
    
    for i in range(len(rows) - 1, -1, -1):
        for j in range(len(rows[i]) - 1, -1, -1):
            if rows[i][j] == "":
                rows[i].pop(j)
        
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if i != 0 and rows[i][j] != "":
                rows[i][j] = rows[i][j].strip()
                
    for i in range(len(rows) - 1, -1, -1):
        for j in range(len(rows[i])- 1, -1, -1):
            if rows[i][j] == "":
                rows.pop(i)
    
    for j in range(len(rows[0])):
        column = []
        for i in range(len(rows)):
            column.append(rows[i][j])
        columns.append(column)

    for i in range(len(columns)):
        for j in range(len(columns[i])):
            if j != 0:
                columns[i][j] = float(columns[i][j])
         
    for i in range(1, len(columns[0])):
        absolutes.append(absolute(columns[1][i], columns[4][i]))
        
    columns.append(absolutes)
    
    plt.figure(dpi = 500)
    
    for i in range(1, len(columns[0])):
        plt.xlabel("Color (B-V)")
        plt.ylabel("Absolute Magnitude")
        plt.plot(columns[8][i], columns[9][i], "o", color = "black", 
                 ms = 0.5)
    
main()
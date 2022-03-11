rows = []

def main():
    with open("HIP_star_data.txt", "r") as infile:
        while True:
            row = infile.readline()
            if row == "":
                break
            else:
                rows.append(row)
                
    print(rows)

    for i in range(len(rows)):
        rows[i] = rows[i].split(sep = " ")
    
    for i in range(len(rows) - 1, -1, -1):
        for j in range(len(rows[i]) - 1, -1, -1):
            if rows[i][j] == "":
                rows[i].pop(j)
            if i == 0:
                columns = rows[i]
                rows.pop(i)
            else:
                rows[i][j] = rows[i][j].strip()
        
    
    
main()
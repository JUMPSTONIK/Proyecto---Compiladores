def extraction(line):
    firstcut = line.find("=")
    id = line[:firstcut]
    #print("id: " + id)
    terminal = line[firstcut + 1:] 
    #print("terminal: " + terminal)
    return id, terminal

def getText(fileName):
    f = open(fileName, "r")
    COCOr = f.read()
    f.close()
    return COCOr
import os

def clear():
    os.system("clear")

def write2file(filename,text):
    fFile = open(filename,'a')
    fFile.write(text)
    fFile.close()

def importList(filename):
    with open(filename) as file:
        lines = [line.strip() for line in file]
        return lines

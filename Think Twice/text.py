def changeLevel():
    #读取record.txt里的值并清空
    with open('assets/pictures/adventure/Level/record.txt','r') as f:
        record=f.read()
    with open('assets/pictures/adventure/Level/record.txt','w') as f:
        f.write(str(int(record) - 1))

changeLevel()